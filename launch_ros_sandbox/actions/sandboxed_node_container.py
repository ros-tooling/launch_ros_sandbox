# Copyright FIXME

from typing import List
from typing import Optional

from launch import Action
from launch import LaunchContext
from launch.some_substitutions_type import SomeSubstitutionsType
from launch.substitution import Substitution
from launch.utilities import normalize_to_list_of_substitutions

from launch_ros_sandbox.descriptions import SandboxedNode

""" 
Module for SandboxedNodeContainer class.
"""

class SandboxedNodeContainer(Action):
    """
    SandboxedNodeContainer
    """

    def __init__(
        self,
        *,
        sandbox_name: Optional[SomeSubstitutionsType] = None,
        node_descriptions: Optional[List[SandboxedNode]] = None,
        **kwargs
    ) -> None:
        """
        Initializes the SandboxedNodeContainer
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
        Executes the SandboxedNodeContainer
        """

        pass

    @property
    def sandbox_name(self) -> List[Substitution]:
        """ Get sandbox name as a sequence of substitutions to be performed. """
        return self.__sandbox_name
