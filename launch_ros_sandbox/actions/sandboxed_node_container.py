# Copyright FIXME

"""Module for SandboxedNodeContainer class."""

from typing import List
from typing import Optional

from launch import Action
from launch import LaunchContext
from launch.some_substitutions_type import SomeSubstitutionsType
from launch.substitution import Substitution
from launch.utilities import normalize_to_list_of_substitutions

from launch_ros_sandbox.descriptions import SandboxedNode


class SandboxedNodeContainer(Action):
    """SandboxedNodeContainer is an action that launches nodes within a sandboxed environment."""

    def __init__(
        self,
        *,
        sandbox_name: Optional[SomeSubstitutionsType] = None,
        policy=None,
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
            self.__sandbox_name = normalize_to_list_of_substitutions(sandbox_name)

        self.__node_descriptions = None
        if node_descriptions is not None:
            self.__node_descriptions = node_descriptions

    def execute(
        self,
        context: LaunchContext
    ) -> Optional[List[Action]]:
        """
        Execute the SandboxedNodeContainer.

        All node descriptions defined will be launched inside the sandbox defined by the policy.
        """
        pass

    @property
    def sandbox_name(self) -> List[Substitution]:
        """Get sandbox name as a sequence of substitutions to be performed."""
        return self.__sandbox_name
