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
Minimal example for using SandboxedNodeContainer with DockerPolicy with limited CPU.

This example runs a ROS 2 node in a sandboxed environment by invoking SandboxedNodeContainer
action. SandboxedNodeContainer delegates the launch parameters to an instance of launch_ros that is
running in a Docker container.

Currently, this test will only launch the Talker demo node inside Docker. This node can be observed
by launching a Listener node either within the same docker container or on the host machine. The
Docker container must be stopped externally in order to free resources.

"container_id" should be substituted for the container name logged by launch. It can also be found
by running "docker container ls".

How to stop the Docker container:
- docker stop $container_id

How to run listener inside the Docker container
- docker exec -it $container_id /bin/bash
- source /ros_entrypoint.sh
- ros2 run demo_nodes_cpp listener
"""

import sys

from launch import LaunchDescription
from launch import LaunchService

from launch_ros_sandbox.actions import SandboxedNodeContainer
from launch_ros_sandbox.descriptions import DockerPolicy
from launch_ros_sandbox.descriptions import SandboxedNode


def generate_launch_description() -> LaunchDescription:
    """
    Create a launch description for starting SandboxedNodeContainer with DockerPolicy.

    In this example, the C++ demo talker node is loaded inside the SandboxedNodeContainer called
    'sandboxed-listener-node'.
    The Docker policy uses a Docker image of ROS2 Dashing (Desktop) from 'osrf/ros'.
    When the sandboxed node is executed, it runs the ROS 2 node within the Docker container.
    The container continues to run until stopped externally.
    The talker node can be interacted with by launching a listener node.
    The listener node does not need to be launched from within the Docker container.
    Only CPU 0 will be available to the nodes.
    The number of CPUs can be queried by running nproc inside the container.
    """
    ld = LaunchDescription()

    ld.add_action(
        SandboxedNodeContainer(
            sandbox_name='my_sandbox',
            policy=DockerPolicy(
                tag='dashing-desktop',
                repository='osrf/ros',
                container_name='sandboxed-listener-node',
                run_args={
                    'cpuset_cpus': '0'
                }
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
    """Starts the SandboxedNodeContainer example as a script."""

    ls = LaunchService(argv=sys.argv[1:], debug=True)
    ls.include_launch_description(generate_launch_description())
    sys.exit(ls.run())
