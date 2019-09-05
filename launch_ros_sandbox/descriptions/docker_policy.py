# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Module for DockerPolicy."""

import time
from typing import List
from typing import Optional

import docker
from docker.errors import ImageNotFound

import launch
from launch import LaunchContext
from launch.utilities import perform_substitutions

from launch_ros.substitutions import ExecutableInPackage

from launch_ros_sandbox.descriptions import SandboxedNode

DEFAULT_DOCKER_REPO = 'osrf/ros'
DEFAULT_DOCKER_TAG = 'dashing-desktop'


class DockerPolicy:
    """DockerPolicy defines parameters for running a sandboxed node in a Docker container."""

    def __init__(
        self,
        *,
        repository: Optional[str] = None,
        tag: Optional[str] = None,
    ) -> None:
        """Construct the DockerPolicy."""
        # Set the logger
        self.__logger = launch.logging.get_logger(__name__)
        # Default to latest if only a repository is provided
        if repository is not None and tag is None:
            self._tag = 'latest'
        else:
            self._repository = DEFAULT_DOCKER_REPO if repository is None else repository
            self._tag = DEFAULT_DOCKER_TAG if tag is None else tag
        # Format image name
        self._image_name = '{}:{}'.format(self._repository, self._tag)
        # Create low-level Docker client for streaming logs (Mac/Ubuntu only)
        self._low_docker_client = docker.APIClient(
            base_url='unix://var/run/docker.sock')
        self._docker_client = docker.from_env()
        self._execution_list = []
        self._container = None
        self._load_docker_container()

    def _load_docker_container(self) -> None:
        """Pull an image and then run the container."""
        try:
            # Pull the image first. Will update if already pulled.
            self.__logger.debug('Pulling image...')
            self._docker_client.images.pull(
                repository=self._repository,
                tag=self._tag
            )
            self.__logger.debug('Image Pulled')
            # Run the container and keep track of its ID.
            self._container = self._docker_client.containers.run(
                image=self._image_name,
                detach=True,
                auto_remove=True,
                name='ros2launch-sandboxed-node-{}'.format(
                    time.strftime('%H%M%S'))
            )
        except ImageNotFound:
            available_images = self._low_docker_client.images()
            self.__logger.exception('Could not find the Docker image with name: {}.\nThe only '
                                    'images available are:\n{}'
                                    .format(self._image_name, '\n'.join(available_images)))

    @property
    def docker_client(self) -> docker.DockerClient:
        """Return an instance of the Docker client."""
        return self._docker_client

    def apply(
        self,
        context: LaunchContext,
        node_descriptions: List[SandboxedNode]
    ) -> None:
        """
        Execute each node in the Docker container.

        This function in its current state will assume that the path of the
        executable on the host the launch file is run on is the same as the path
        in the Docker container (ex. /opt/ros/dashing/lib).
        TODO: Create a Launch agent in the docker container that can perform the
              substitutions correctly.
        """
        self.__logger.info('Executing nodes in Docker container...')
        for description in node_descriptions:
            package_name = perform_substitutions(
                context,
                description.package
            )
            executable_name = perform_substitutions(
                context,
                description.node_executable
            )
            cmd = ExecutableInPackage(
                package=package_name,
                executable=executable_name
            ).perform(context)

            if self._container is not None:
                exit_code, output = self._container.exec_run(cmd=cmd)
                self.__logger.debug('Executed command: {}\nStatus code: {}\nOutput: {}'
                                    .format(cmd, exit_code, output))
