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

"""
Module for the DockerPolicy description.

Using DockerPolicy, users can load one or more nodes into a particular Docker container. Using
DockerPolicy requires that Docker 18+ and docker-py 4.0+ is installed.

Example:
    ld = launch.LaunchDescription()

    ld.add_action(
        launch_ros_sandbox.actions.SandboxedNodeContainer(
            sandbox_name='my_sandbox',
            policy=launch_ros_sandbox.descriptions.DockerPolicy(),
            node_descriptions=[
                launch_ros_sandbox.descriptions.SandboxedNode(
                    package='demo_nodes_cpp',
                    node_executable='talker',
                ),
                launch_ros_sandbox.descriptions.SandboxedNode(
                    package='demo_nodes_cpp',
                    node_executable='listener'
                )
            ]
        )
    )

This will launch the talker and listener nodes within a Docker container running
'osrf/ros:dashing-desktop' image.

Currently persistence is not supported, however it is planned to support forwarding all run
parameters to docker-py.
"""

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

_DEFAULT_DOCKER_REPO = 'osrf/ros'
_DEFAULT_DOCKER_TAG = 'dashing-desktop'


def _generate_container_name() -> str:
    """Generate a Docker container name for use in DockerPolicy."""
    return 'ros2launch-sandboxed-node-{}'.format(time.strftime('%H%M%S'))


class DockerPolicy:
    """
    DockerPolicy defines parameters for running a sandboxed node in a Docker container.

    All of the parameters passed into DockerPolicy are immutable and only processed once the
    SandboxedNodeContainer is executed.
    """

    def __init__(
        self,
        *,
        repository: Optional[str] = None,
        tag: Optional[str] = None,
    ) -> None:
        """
        Construct the DockerPolicy.

        All of the parameters are preserved if they were set.

        :param: repository is the Docker repository to pull the image from. 'repository' defaults to
        'osrf/ros'.
        :param: tag is the Docker image tag. 'tag' defaults to 'dashing-desktop' if 'repository'
        evaluates to 'osrf/ros'; this includes if 'repository' defaults to 'osrf/ros'. Otherwise
        'tag' defaults to 'latest'.
        """
        self.__logger = launch.logging.get_logger(__name__)

        # calculate the actual tag and repository based on if either are set.
        if repository is not None:
            if tag is not None:
                self._repository = repository
                self._tag = tag
            else:
                self._repository = repository
                self._tag = 'latest'
        elif tag is not None:
            self._repository = _DEFAULT_DOCKER_REPO
            self._tag = tag
        else:
            self._repository = _DEFAULT_DOCKER_REPO
            self._tag = _DEFAULT_DOCKER_TAG

        self._image_name = '{}:{}'.format(self._repository, self._tag)
        self._container = None
        self._container_name = ''

    def _load_docker_container(self) -> None:
        """Pull an image and then run the container."""
        # Create low-level Docker client for streaming logs (Mac/Ubuntu only)
        self._low_docker_client = docker.APIClient(base_url='unix://var/run/docker.sock')
        self._docker_client = docker.from_env()
        self._container_name = _generate_container_name()

        try:
            # Pull the image first. Will update if already pulled.
            self.__logger.debug('Pulling image {}'.format(self._image_name))
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
                name=self.container_name
            )
        except ImageNotFound:
            available_images = self._low_docker_client.images()
            self.__logger.exception('Could not find the Docker image with name: {}.\nThe only '
                                    'images available are:\n{}'
                                    .format(self._image_name, '\n'.join(available_images)))

    @property
    def container_name(self) -> str:
        """Return the Docker container name."""
        return self._container_name

    @property
    def docker_client(self) -> docker.DockerClient:
        """Return the Docker client."""
        return self._docker_client

    @property
    def repository(self) -> str:
        """Return the Docker image repository."""
        return self._repository

    @property
    def tag(self) -> str:
        """Return the Docker image tag."""
        return self._tag

    @property
    def image_name(self) -> str:
        """
        Return the Docker image name.

        The image name is defined as 'repository:tag'.
        """
        return '{}:{}'.format(self.repository, self.tag)

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
        if self._container is None:
            self._load_docker_container()

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
