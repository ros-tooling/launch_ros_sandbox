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

LoadDockerNodes is an Action that controls the lifecycle of a sandboxed environment running nodes as
a Docker container. This Action is not exported and should only be used internally.
"""

from asyncio import Future
from typing import List
from typing import Optional

from launch import Action
from launch import LaunchContext


class LoadDockerNodes(Action):
    """
    LoadDockerNodes is an Action that controls the sandbox environment spawned by `DockerPolicy`.

    LoadDockerNodes should only be constructed by `DockerPolicy.apply`.
    TODO: Move the logic for launching the sandbox environment into `LoadDockerNodes.execute`
    """

    def _start_docker_container(self) -> None:
        """Start Docker container."""
        pass

    def _load_nodes_in_docker(self) -> None:
        """Load all nodes into Docker container."""
        pass

    def get_asyncio_future(self) -> Optional[Future]:
        """Return the asyncio Future that represents the lifecycle of the Docker container."""
        return None

    def execute(
        self,
        context: LaunchContext
    ) -> Optional[List[Action]]:
        """
        Execute the ROS 2 sandbox inside Docker.

        This will start the Docker container and run each ROS 2 node from inside that container.
        There is no additional work required, so this function always returns None.
        """
        return None
