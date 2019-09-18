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

The unit tests verify that tag and repository properly default. No actual processing occurs inside
DockerPolicy's constructor, so there is no side effects on calling the constructors within these
tests. These tests also do not require the Docker daemon since DockerPolicy does not interact
with Docker until the policy is applied to the SandboxedNodeContainer.
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

        assert docker_policy.image_name == 'osrf/ros:dashing-desktop'
        assert docker_policy.repository == 'osrf/ros'
        assert docker_policy.tag == 'dashing-desktop'

    def test_tag_defaults_to_latest_if_repository_is_defined(self) -> None:
        """Verify DockerPolicy tag defaults to 'latest' when only repository is specified."""
        docker_policy = DockerPolicy(repository='ubuntu')

        assert docker_policy.image_name == 'ubuntu:latest'
        assert docker_policy.repository == 'ubuntu'
        assert docker_policy.tag == 'latest'

    def test_repository_defaults_to_osrf_if_tag_is_defined(self) -> None:
        """Verify DockerPolicy repository defaults to 'osrf/ros' if tag is defined."""
        docker_policy = DockerPolicy(tag='crystal-desktop')

        assert docker_policy.image_name == 'osrf/ros:crystal-desktop'
        assert docker_policy.repository == 'osrf/ros'
        assert docker_policy.tag == 'crystal-desktop'

    def test_image_name_properly_set_if_tag_and_repository_are_defined(self) -> None:
        """Verify DockerPolicy image_name is 'repository:tag' if both are defined."""
        docker_policy = DockerPolicy(
            repository='ubuntu',
            tag='bionic'
        )

        assert docker_policy.image_name == 'ubuntu:bionic'
        assert docker_policy.repository == 'ubuntu'
        assert docker_policy.tag == 'bionic'

    def test_tag_defaults_to_dashing_desktop_if_repository_is_manually_set(self) -> None:
        """Verify DockerPolicy tag defaults to 'dashing-desktop' if repository is 'osrf/ros'."""
        docker_policy = DockerPolicy(
            repository='osrf/ros',
        )

        assert docker_policy.image_name == 'osrf/ros:dashing-desktop'
        assert docker_policy.repository == 'osrf/ros'
        assert docker_policy.tag == 'dashing-desktop'

    def test_entrypoint_assign_default_repo_default_tag(self) -> None:
        """Verify entrypoint can be set if repo and tag are defaults."""
        docker_policy = DockerPolicy(
            entrypoint='foo'
        )

        assert docker_policy.entrypoint == 'foo'
        assert docker_policy.repository == 'osrf/ros'
        assert docker_policy.tag == 'dashing-desktop'

    def test_entrypoint_assign_default_repo(self) -> None:
        """Verify entrypoint can be set if repo is default."""
        docker_policy = DockerPolicy(
            entrypoint='foo',
            tag='bar'
        )

        assert docker_policy.entrypoint == 'foo'
        assert docker_policy.repository == 'osrf/ros'
        assert docker_policy.tag == 'bar'

    def test_entrypoint_assign_default_tag(self) -> None:
        """Verify entrypoint can be set if tag is default."""
        docker_policy = DockerPolicy(
            entrypoint='foo',
            repository='bar'
        )

        assert docker_policy.entrypoint == 'foo'
        assert docker_policy.repository == 'bar'
        assert docker_policy.tag == 'latest'

    def test_entrypoint_default_osrf_repo(self) -> None:
        """Verify entrypoint is 'ros_entrypoint' if repo is set to 'osrf/ros'."""
        docker_policy = DockerPolicy(
            repository='osrf/ros'
        )

        assert docker_policy.repository == 'osrf/ros'
        assert docker_policy.entrypoint == '/ros_entrypoint.sh'

    def test_entrypoint_default_not_osrf_repo(self) -> None:
        """Verify entrypoint is '/bin/bash -c' if repo is set to not 'osrf/ros'."""
        docker_policy = DockerPolicy(
            repository='foo'
        )

        assert docker_policy.repository == 'foo'
        assert docker_policy.entrypoint == '/bin/bash -c'

    def test_run_args_set_correctly(self) -> None:
        """Verify the DockerPolicy run arguments match for the Docker Image."""
        run_args = {
                'cpuset_cpus': 0,
                'mem_limit': '128m'
            }
        docker_policy = DockerPolicy(
            run_args=run_args
        )

        assert docker_policy.run_args == run_args

    def test_empty_run_args_set_correctly(self) -> None:
        """Verify the DockerPolicy has no run args if not set."""
        docker_policy = DockerPolicy()

        assert docker_policy.run_args is None
