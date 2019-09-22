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
--------

.. code-block:: python

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
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import launch
from launch import Action
from launch import LaunchContext

from launch_ros_sandbox.descriptions.policy import Policy
from launch_ros_sandbox.descriptions.sandboxed_node import SandboxedNode

_DEFAULT_DOCKER_REPO = 'osrf/ros'
_DEFAULT_DOCKER_TAG = 'dashing-desktop'
_DEFAULT_EXEC_ENTRYPOINT = '/ros_entrypoint.sh'


def _generate_container_name() -> str:
    """Generate a Docker container name for use in DockerPolicy."""
    return 'ros2launch-sandboxed-node-{}'.format(time.strftime('%H%M%S'))


class DockerPolicy(Policy):
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
        run_args: Optional[Dict[str, Any]] = None,
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
        :param: run_args is a dictionary of arguments (str to Any) passed into the 'run' command
        for the Docker container. See [1] for supported arguments.
        'image', 'tty', 'detach', 'auto_remove', and 'name' are not valid keywords for 'run_args'
        due to being defined by LoadDockerNodes.

         [1]: https://docker-py.readthedocs.io/en/stable/containers.html#docker.models.containers.ContainerCollection.run # noqa
        """
        self.__logger = launch.logging.get_logger(__name__)

        # Evaluate repository first since the evaluation of tag and entrypoint depend upon it.
        self._repository = repository or _DEFAULT_DOCKER_REPO

        if self._repository == _DEFAULT_DOCKER_REPO:
            self._tag = tag or _DEFAULT_DOCKER_TAG
            self._entrypoint = entrypoint or _DEFAULT_EXEC_ENTRYPOINT
        else:
            # Repository is not the default repo, so assume we're not using an osrf image. This
            # changes the default tag to be the conventional 'latest' and default entrypoint to be
            # bash.
            self._tag = tag or 'latest'
            self._entrypoint = entrypoint or '/bin/bash -c'

        self._image_name = '{}:{}'.format(self._repository, self._tag)
        self._container_name = container_name or _generate_container_name()
        self._run_args = run_args

    @property
    def entrypoint(self) -> str:
        """Return the Docker container entrypoint."""
        return self._entrypoint

    @property
    def container_name(self) -> str:
        """Return the Docker container name."""
        return self._container_name

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

    @property
    def run_args(self) -> Optional[Dict[str, Any]]:
        """Return the dictionary of Docker container run arguments."""
        return self._run_args

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
        from launch_ros_sandbox.actions.load_docker_nodes import LoadDockerNodes

        return LoadDockerNodes(
            policy=self,
            node_descriptions=node_descriptions
        )
