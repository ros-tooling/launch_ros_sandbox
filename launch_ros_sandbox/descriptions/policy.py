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
Module for Policy description.

Policy represents a security policy that can be applied to a SandboxedNodeContainer. It provides a
single method `apply` which performs the sandboxing on the ROS 2 nodes described by
SandboxedNodeContainer. The `apply` method must be implemented by any security policy that extends
Policy.

"""

from abc import ABC
from abc import abstractmethod
from typing import List

from launch import Action
from launch import LaunchContext

from launch_ros_sandbox.descriptions.sandboxed_node import SandboxedNode


class Policy(ABC):
    """Policy is the base class used by any sandboxing Policy description."""

    @abstractmethod
    def apply(
        self,
        context: LaunchContext,
        node_descriptions: List[SandboxedNode]
    ) -> Action:
        """
        Apply the sandboxing policy and returns an Action for controlling the environment.

        This method is called by `SandboxedNodeContainer.execute` when the SandboxedNodeContainer
        Action is visited by the LaunchService. This function returns a single Action which will
        launch the nodes inside the sandboxed environment. LaunchService monitors the lifecycle of
        this Action.

        :param: context is the LaunchContext. This is forwarded by SandboxedNodeContainer and is
        used to resolve any substitutions.
        :param: node_descriptions is the List of ROS 2 nodes to run within the sandboxed
        environment. This policy should handle launching each of these nodes within the sandbox.
        """
        pass
