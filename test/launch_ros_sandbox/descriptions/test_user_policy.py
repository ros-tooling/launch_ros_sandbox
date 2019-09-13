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

"""Tests for the UserPolicy description."""

import os

import unittest

from launch_ros_sandbox.descriptions import UserPolicy


class TestUserPolicy(unittest.TestCase):

    def test_defaults_to_current_user(self):
        """Verify UserPolicy.run_as defaults to current user."""
        current_uid = os.getuid()
        current_gid = os.getgid()

        user_policy = UserPolicy()
        assert current_uid == user_policy.run_as.uid
        assert current_gid == user_policy.run_as.gid
