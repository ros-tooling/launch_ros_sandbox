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

"""Tests for User."""

import getpass
import os

import unittest

from launch_ros_sandbox.descriptions import User


class TestUser(unittest.TestCase):

    def test_get_user_from_username(self):
        """Verify User.from_username returns the correct User."""
        uid = os.getuid()
        gid = os.getgid()
        username = getpass.getuser()
        user = User.from_username(username)

        assert uid == user.uid
        assert gid == user.gid
