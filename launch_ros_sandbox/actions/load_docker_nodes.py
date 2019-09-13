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
Internal module for the LoadDockerNodes Action.

LoadDockerNodes is an Action that controls the lifecycle of a sandboxed environment running nodes
as a Docker container. This Action is not exported and should only be used internally.
"""

from asyncio import CancelledError, Future

from threading import Lock
from typing import List, Optional

import docker

import launch
from launch import Action, LaunchContext
from launch.event import Event
from launch.event_handlers import OnShutdown
from launch.some_actions_type import SomeActionsType
from launch.utilities import create_future, perform_substitutions

from launch_ros_sandbox.descriptions.docker_policy import DockerPolicy
from launch_ros_sandbox.descriptions.sandboxed_node import SandboxedNode


def _containerized_cmd(entrypoint: str, package: str, executable: str) -> List[str]:
    """Prepare the command for executing within the Docker container."""
    # Use ros2 CLI command to find the executable
    return [entrypoint, 'ros2', 'run', package, executable]


def _get_none_container() -> Optional[docker.models.containers.Container]:
    """
    Return None.

    Workaround for Python3.5 compliance, since we can't hint member variable types until 3.6
    This lets us initialize a member variable as None but still note its type for mypy.
    """
    return None


class LoadDockerNodes(Action):
    """
    LoadDockerNodes is an Action that controls the sandbox environment spawned by `DockerPolicy`.

    LoadDockerNodes should only be constructed by `DockerPolicy.apply`.
    """

    def __init__(
        self,
        policy: DockerPolicy,
        node_descriptions: List[SandboxedNode],
        **kwargs
    ) -> None:
        """
        Construct the LoadDockerNodes Action.

        Parameters regarding initialization are copied here.
        Most of the arguments are forwarded to Action.
        """
        super().__init__(**kwargs)
        self._policy = policy
        self._node_descriptions = node_descriptions
        self._completed_future = None
        self._started_task = None
        self._container = None
        self._shutdown_lock = Lock()
        self._docker_client = docker.from_env()
        self.__logger = launch.logging.get_logger(__name__)

    def _pull_docker_image(self) -> None:
        """
        Pull the docker image.

        This will download the Docker image if it is not currently cached and will update it if its
        out of date.

        :raises ImageNotFound if Docker cannot find the remote repo for the image to pull
        """
        self.__logger.debug('Pulling image {}'.format(self._policy.image_name))

        # This method may throw an ImageNotFound exception. Let the exception propogate upwards
        # since further operations should not continue
        self._docker_client.images.pull(
            repository=self._policy.repository,
            tag=self._policy.tag
        )

    def _start_docker_container(self) -> None:
        """Start Docker container."""
        self._container = self._docker_client.containers.run(
            image=self._policy.image_name,
            detach=True,
            auto_remove=True,
            tty=True,
            name=self._policy.container_name
        )

        self.__logger.debug('Running Docker container: \"{}\"'.format(self._policy.container_name))

    def _load_nodes_in_docker(
        self,
        context: LaunchContext
    ) -> None:
        """Load all nodes into Docker container."""
        if self._container is None:
            self.__logger.error('Unable to load nodes into Docker container: '
                                'no active Docker container!')
            return

        for description in self._node_descriptions:
            package_name = perform_substitutions(
                context=context,
                subs=description.package
            )

            executable_name = perform_substitutions(
                context=context,
                subs=description.node_executable
            )

            cmd = _containerized_cmd(
                entrypoint=self._policy.entrypoint,
                package=package_name,
                executable=executable_name
            )

            self._container.exec_run(
                cmd=cmd,
                detach=True,
                tty=True,
            )

            self.__logger.debug('Running \"{}\" in container: \"{}\"'
                                .format(cmd, self._policy.container_name))

    async def _start_docker_nodes(
        self,
        context: LaunchContext
    ) -> None:
        """Start the Docker container and load all nodes into it.

        This will first attempt to pull the docker image, start the docker container, and then load
        all of the nodes.

        """
        self._pull_docker_image()

        self._start_docker_container()

        self._load_nodes_in_docker(context)

    def get_asyncio_future(self) -> Optional[Future]:
        """Return the asyncio Future that represents the lifecycle of the Docker container."""
        return self._completed_future

    def execute(
        self,
        context: LaunchContext
    ) -> Optional[List[Action]]:
        """
        Execute the ROS 2 sandbox inside Docker.

        This will start the Docker container and run each ROS 2 node from inside that container.
        There is no additional work required, so this function always returns None.
        """
        context.register_event_handler(
            OnShutdown(
                on_shutdown=self.__on_shutdown
            )
        )

        self._completed_future = create_future(context.asyncio_loop)

        self._started_task = context.asyncio_loop.create_task(
            self._start_docker_nodes(context)
        )

        return None

    def __on_shutdown(
        self,
        event: Event,
        context: LaunchContext
    ) -> Optional[SomeActionsType]:
        """Run when the shutdown signal has been received.

        This will cancel the started task, if running, call cancel
        on the completed future, and stop the container.

        """
        with self._shutdown_lock:

            # if still starting cancel
            if self._started_task is not None:
                try:
                    self._started_task.cancel()
                except CancelledError:
                    self._started_task = None

            if self._completed_future is not None:
                self._completed_future.cancel()
                self._completed_future = None

                if self._container is not None:
                    self._container.stop()
                    self._container = None
