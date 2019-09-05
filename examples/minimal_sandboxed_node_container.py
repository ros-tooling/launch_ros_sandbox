#!/usr/bin/env python3

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
Minimal example for using SandboxedNodeContainer.

This example runs a ROS 2 node in a sandboxed environment by invoking SandboxedNodeContainer
action. SandboxedNodeContainer delegates the launch parameters to an instance of launch_ros that is
running in a sandboxed environment using the requested sandboxing policy.
"""

import sys

import launch

import launch_ros_sandbox


def generate_launch_description() -> launch.LaunchDescription:
    """
    Create launch description for starting SandboxedNodeContainer.

    Two nodes are loaded into the sandboxed container: talker and listener.
    No operation is performed since no sandboxing policy was defined.
    """
    ld = launch.LaunchDescription()

    ld.add_action(
        launch_ros_sandbox.actions.SandboxedNodeContainer(
            sandbox_name='my_sandbox',
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

    return ld


if __name__ == '__main__':
    """Starts the SandboxedNodeContainer example as a script."""

    ls = launch.LaunchService(argv=sys.argv[1:])
    ls.include_launch_description(generate_launch_description())
    sys.exit(ls.run())
