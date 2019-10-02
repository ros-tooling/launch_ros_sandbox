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
Minimal example for demoing when an image not found locally nor on DockerHub is ran in DockerPolicy.

This example tries to run a ROS 2 node in a Docker container that should not exist locally nor on
DockerHub. The expected behavior is that launch logs to warn that the Image is not found and then
logs to error that it is also not found.
"""
import sys

from launch import LaunchDescription, LaunchService

from launch_ros_sandbox.actions import SandboxedNodeContainer
from launch_ros_sandbox.descriptions import DockerPolicy
from launch_ros_sandbox.descriptions import SandboxedNode


def generate_launch_description():
    """
    Create launch description for starting a SandboxedNodeContainer with a bad image name.

    A SandboxedNode must be loaded into the container for any work to be done.
    """
    ld = LaunchDescription()
    ld.add_action(
        SandboxedNodeContainer(
            sandbox_name='my_sandbox',
            policy=DockerPolicy(
                tag='not-exist',
                repository='definitely-not-a-real-image',
            ),
            node_descriptions=[
                SandboxedNode(
                    package='demo_nodes_cpp',
                    node_executable='talker',
                ),
            ]
        )
    )

    return ld


if __name__ == '__main__':
    ls = LaunchService(argv=sys.argv[1:], debug=True)
    ls.include_launch_description(generate_launch_description())
    sys.exit(ls.run())
