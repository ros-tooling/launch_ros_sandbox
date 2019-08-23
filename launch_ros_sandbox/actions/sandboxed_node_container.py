# Copyright FIXME

from typing import List
from typing import Optional

from launch import Action
from launch import LaunchContext

""" 
Module for SandboxedNodeContainer class.
"""

class SandboxedNodeContainer(Action):
    """
    SandboxedNodeContainer
    """

    def __init__(
        self,
        **kwargs
    ) -> None:
        """
        Initializes the SandboxedNodeContainer
        """

        super().__init__(**kwargs)
    
    def execute(
        self, 
        context: LaunchContext
    ) -> Optional[List[Action]]:
        """
        Executes the SandboxedNodeContainer
        """

        pass

    