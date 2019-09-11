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
from launch import Action
from launch import LaunchContext
from launch.utilities import perform_substitutions

from launch_ros_sandbox.descriptions.policy import Policy
from launch_ros_sandbox.descriptions.sandboxed_node import SandboxedNode

_DEFAULT_DOCKER_REPO = 'osrf/ros'
_DEFAULT_DOCKER_TAG = 'dashing-desktop'
_DEFAULT_EXEC_ENTRYPOINT = '/ros_entrypoint.sh'


def _containerized_cmd(entrypoint: str, package: str, executable: str) -> List[str]:
    """Prepare the command for executing within the Docker container."""
    # Use ros2 CLI command to find the executable
    return [entrypoint, 'ros2', 'run', package, executable]


def _generate_container_name() -> str:
    """Generate a Docker container name for use in DockerPolicy."""
    return 'ros2launch-sandboxed-node-{}'.format(time.strftime('%H%M%S'))


class DockerPolicy:
    """
    DockerPolicy defines parameters for running a sandboxed node in a Docker container.

    DockerPolicy extends Policy. All of the parameters passed into DockerPolicy are immutable and
    only processed once the SandboxedNodeContainer is executed.
    """

    def __init__(
        self,
        *,
        repository: Optional[str] = None,
        tag: Optional[str] = None,
        entrypoint: Optional[str] = None,
        container_name: Optional[str] = None,
    ) -> None:
        """
        Construct the DockerPolicy.

        The constructor sets the repository, tag, and entrypoint for the Docker container based on
        the provided parameters. The repository and tag parameters are optional and will default
        to OSRF's latest ROS distribution if not set. A container name can also be provided, but
        will default to a generic name. The container is not started until the policy is applied.

        :param: repository is the Docker repository to pull the image from. 'repository' defaults
        to 'osrf/ros'.
        :param: tag is the Docker image tag. 'tag' defaults to 'dashing-desktop' if 'repository'
        evaluates to 'osrf/ros'; this includes if 'repository' defaults to 'osrf/ros'. Otherwise
        'tag' defaults to 'latest'.
        :param: entrypoint is the absolute path of the script to run within the Docker container
        for launching internal ROS 2 nodes. Defaults to '/ros_entrypoint.sh' if repository
        evaluates to 'osrf/ros'. Otherwise 'entrypoint' defaults to '/bin/bash -c'.
        :param: container_name is the name of the container passed to Docker to make it easier to
        identify when listing all the containers. Defaults to
        ros2launch-sandboxed-node-<Hour><Minute><Sec> where the time is when the DockerPolicy
        was constructed.
        """
        self.__logger = launch.logging.get_logger(__name__)

        # Calculate the actual tag and repository based on if either are set.
        if repository is not None:
            if repository == _DEFAULT_DOCKER_REPO:
                self._tag = tag or _DEFAULT_DOCKER_REPO
            else:
                self._tag = tag or 'latest'
        elif tag is not None:
            self._repository = _DEFAULT_DOCKER_REPO
            self._tag = tag
        else:
            self._repository = _DEFAULT_DOCKER_REPO
            self._tag = _DEFAULT_DOCKER_TAG

        if entrypoint is not None:
            self._entrypoint = entrypoint
        elif self._repository == _DEFAULT_DOCKER_REPO:
            self._entrypoint = _DEFAULT_EXEC_ENTRYPOINT
        else:
            self._entrypoint = '/bin/bash -c'

        self._image_name = '{}:{}'.format(self._repository, self._tag)
        self._container = None
        self._container_name = container_name or _generate_container_name()

    def _load_docker_container(self) -> None:
        """Pull an image and then run the container."""
        # Create low-level Docker client for streaming logs (Mac/Ubuntu only)
        self._low_docker_client = docker.APIClient(base_url='unix://var/run/docker.sock')
        self._docker_client = docker.from_env()

        try:
            # Pull the image first. Will update if already pulled.
            self.__logger.debug('Pulling image {}'.format(self._image_name))
            self._docker_client.images.pull(
                repository=self._repository,
                tag=self._tag
            )

            # Run the container and keep track of its ID.
            self._container = self._docker_client.containers.run(
                image=self._image_name,
                detach=True,
                auto_remove=True,
                tty=True,
                name=self.container_name
            )

            self.__logger.info('Running Docker container: \"{}\"'.format(self.container_name))
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
    ) -> Action:
        """
        Apply the policy and load each node inside the Docker sandbox.

        Applying the policy involves iterating over the list of nodes to execute and using the
        `ros2 run` CLI within the container. The node and package names are resolved using
        substitutions, a utility from Launch.        
        """
        if self._container is None:
            self._load_docker_container()

        for description in node_descriptions:
            package_name = perform_substitutions(
                context,
                description.package
            )

            executable_name = perform_substitutions(
                context,
                description.node_executable
            )

            if self._container is not None:
                cmd = _containerized_cmd(
                    entrypoint=self._entrypoint,
                    package=package_name,
                    executable=executable_name
                )

                exit_code, output = self._container.exec_run(
                    cmd=cmd,
                    detach=True,
                    tty=True
                )

                self.__logger.debug('Executed command: {}'.format(cmd))
                self.__logger.debug('Exit Code: {}'.format(exit_code))
                self.__logger.debug('Output: type={} value={}'.format(type(output), output))
            else:
                self.__logger.error('Could not run cmd: \"package={}, executable={}\" due to there '
                                    'being no active container!'
                                    .format(package_name, executable_name))

        from launch_ros_sandbox.actions.load_docker_nodes import LoadDockerNodes

        # FIXME: Move logic for creating sandbox into LoadDockerNodes.
        return LoadDockerNodes()


Policy.register(DockerPolicy)
