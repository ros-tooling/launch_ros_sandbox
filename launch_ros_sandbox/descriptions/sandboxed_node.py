# Copyright FIXME

""" Module for SandboxedNode. """

from typing import Iterable
from typing import List
from typing import Optional

import launch.logging
from launch.some_substitutions_type import SomeSubstitutionsType
from launch.substitution import Substitution
from launch.utilities import normalize_to_list_of_substitutions

#TODO: this adds dependency on launch_ros; determine if this feature justifies the dependency
from launch_ros.parameters_type import Parameters
from launch_ros.parameters_type import SomeParameters
from launch_ros.remap_rule_type import RemapRules
from launch_ros.remap_rule_type import SomeRemapRules
from launch_ros.utilities import normalize_parameters
from launch_ros.utilities import normalize_remap_rules

class SandboxedNode:
    """
    SandboxedNode describes the launch configurations for a node that will run inside a sandbox environment.
    """
    
    def __init__(
        self,
        *,
        package: SomeSubstitutionsType,
        node_executable: SomeSubstitutionsType,
        node_name: Optional[SomeSubstitutionsType] = None,
        node_namespace: SomeSubstitutionsType = '',
        parameters: Optional[SomeParameters] = None,
        remappings: Optional[SomeRemapRules] = None,
        arguments: Optional[Iterable[SomeSubstitutionsType]] = None,
    ) -> None:
        """
        Constructs a SandboxedNode description.

        The actual node execution is delegated to the sandboxing environment defined by the policy.

        :param: package is the name of the node's package and is required for resolving the node.
        :param: node_executable is the name of the node's executable and is required for resolving the node.
        :param: node_name is an optional name attached to the node when it is launched. Defaults to NONE.
        :param: node_namespace is an optional namespace attached to the node when it is launched. Defaults to empty string.
        :param: parameters are the optional runtime configurations for the node, read from a YAML file. Defaults to NONE.
        :param: remappings are the ordered list of 'to' and 'from' string pairs to be passed to a node as ROS remapping rules.
        """

        self.__package = normalize_to_list_of_substitutions(package)
        self.__node_executable = normalize_to_list_of_substitutions(node_executable)
        
        self.__node_name = None
        if node_name is not None:
            self.__node_name = normalize_to_list_of_substitutions(node_name)
        
        self.__node_namespace = None
        if node_namespace is not None:
            self.__node_namespace = normalize_to_list_of_substitutions(node_namespace)
        
        self.__parameters = None
        if parameters is not None:
            self.__parameters = normalize_parameters(parameters)
        
        self.__remappings = None
        if remappings is not None:
            self.__remappings = normalize_remap_rules(remappings)
        
    @property
    def package(self) -> List[Substitution]:
        """ Get node package name as a sequence of substitutions to be performed. """
        return self.__package

    @property
    def node_executable(self) -> List[Substitution]:
        """ Get node executable name as a sequence of substitutions to be performed. """
        return self.__node_executable
    
    @property
    def node_name(self) -> List[Substitution]:
        """ Get node name as a sequence of substitutions to be performed. """
        return self.__node_name
    
    @property
    def parameters(self) -> Optional[Parameters]:
        """ Get node parameter YAML files or dicts with substitutions to be performed. """
        return self.__parameters
    
    @property
    def remappings(self) -> Optional[RemapRules]:
        """ Get node remapping rules as (from, to) tuples with substitutions to be performed. """
        return self.__remappings
