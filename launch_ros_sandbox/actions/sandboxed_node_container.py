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


"""Module for SandboxedNodeContainer class."""

from typing import List
from typing import Optional

from launch import Action
from launch import LaunchContext
from launch.some_substitutions_type import SomeSubstitutionsType
from launch.substitution import Substitution
from launch.utilities import normalize_to_list_of_substitutions

from launch_ros_sandbox.descriptions import Policy
from launch_ros_sandbox.descriptions import SandboxedNode


class SandboxedNodeContainer(Action):
    """SandboxedNodeContainer is an action that launches nodes within a sandboxed environment."""

    def __init__(
        self,
        *,
        sandbox_name: Optional[SomeSubstitutionsType] = None,
        policy: Optional[Policy] = None,
        node_descriptions: Optional[List[SandboxedNode]] = None,
        **kwargs
    ) -> None:
        """
        Initialize the SandboxedNodeContainer.

        :param: sandbox_name is an optional name assigned to the sandbox environment.
        :param: policy defines the sandboxing strategy used by the sandbox environment.
        :param: node_descriptions are the list of nodes to launch inside the sandbox environment.
        """
        super().__init__(**kwargs)

        self.__sandbox_name = None
        if sandbox_name is not None:
            self.__sandbox_name = normalize_to_list_of_substitutions(
                sandbox_name
            )

        self.__node_descriptions = None
        if node_descriptions is not None:
            self.__node_descriptions = node_descriptions

        self.__policy = policy

    def execute(
        self,
        context: LaunchContext
    ) -> Optional[List[Action]]:
        """
        Execute the SandboxedNodeContainer.

        All node descriptions defined will be launched inside the sandbox defined by the policy.
        """
        if self.__node_descriptions is None:
            return None

        if self.__policy is not None:
            sandboxing_action = self.__policy.apply(
                context=context,
                node_descriptions=self.__node_descriptions
            )

            if sandboxing_action is not None:
                return [sandboxing_action]

        return None

    @property
    def sandbox_name(self) -> Optional[List[Substitution]]:
        """Get sandbox name as a sequence of substitutions to be performed."""
        return self.__sandbox_name
