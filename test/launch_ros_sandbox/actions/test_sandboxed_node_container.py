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

"""Tests for the SandboxedNodeContainer action."""

import unittest.mock

from launch import LaunchDescription
from launch import LaunchService

from launch_ros_sandbox.actions import SandboxedNodeContainer
from launch_ros_sandbox.descriptions import SandboxedNode


class TestSandboxedNodeContainer(unittest.TestCase):

    def _assert_launch_no_errors(self, actions):
        ld = LaunchDescription(actions)
        ls = LaunchService()
        ls.include_launch_description(ld)
        assert 0 == ls.run()

    def _assert_launch_errors(self, actions):
        ld = LaunchDescription(actions)
        ls = LaunchService()
        ls.include_launch_description(ld)
        assert 0 != ls.run()

    def test_launch_nodes(self):
        """Test launching a node."""
        node_action = SandboxedNodeContainer(
            sandbox_name='my_sandbox',
            node_descriptions=[
                SandboxedNode(
                    package='demo_nodes_cpp',
                    node_executable='talker',
                ),
                SandboxedNode(
                    package='demo_nodes_cpp',
                    node_executable='listener',
                ),
            ],
        )
        self._assert_launch_no_errors([node_action])

    def test_launch_empty_nodes(self):
        """Test launching SandboxedNodeContainer without child nodes."""
        node_action = SandboxedNodeContainer(
            sandbox_name='my_sandbox',
        )
        self._assert_launch_no_errors([node_action])

    @unittest.mock.patch('launch_ros_sandbox.descriptions.DockerPolicy')
    def test_launch_docker_policy(self, mock_docker_policy) -> None:
        """Test launching SandboxedNodeContainer with DockerPolicy."""
        node_action = SandboxedNodeContainer(
            sandbox_name='my_sandbox',
            policy=mock_docker_policy,
            node_descriptions=[
                SandboxedNode(
                    package='demo_nodes_cpp',
                    node_executable='talker',
                ),
                SandboxedNode(
                    package='demo_nodes_cpp',
                    node_executable='listener'
                ),
            ],
        )

        self._assert_launch_no_errors([node_action])
        mock_docker_policy.apply.assert_called()
