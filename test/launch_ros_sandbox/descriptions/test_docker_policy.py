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
Tests for the UserPolicy description.

DockerPolicy handles default constructor parameters by setting the image name to
'osrf/ros:dashing-desktop' if both 'repository' and 'tag' are set to the default (None). If only
'tag' is set to its default value, DockerPolicy will assume the tag 'latest'.

The unit tests verify that tag and repository properly default.
"""

import unittest

from launch_ros_sandbox.descriptions import DockerPolicy


class TestDockerPolicy(unittest.TestCase):

    def test_repository_and_tag_defaults_to_osrf_ros_dashing_desktop(self) -> None:
        """
        Verify DockerPolicy 'image_name' is properly resolved with default 'tag' and 'repository'.

        DockerPolicy should resolve 'repository' to 'osrf/ros' and 'tag' to 'desktop-dashing' only
        when both are set to their default (None).
        """
        docker_policy = DockerPolicy()

        assert docker_policy._image_name == 'osrf/ros:dashing-desktop'

    def test_tag_defaults_to_latest(self) -> None:
        """Verify DockerPolicy tag defaults to 'latest' when only repository is specified."""
        docker_policy = DockerPolicy(repository='ubuntu')

        assert docker_policy._image_name == 'ubuntu:latest'
