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
Reference code for spawning a process ran as a different user.

This script creates a User object from the supplied username and runs a subprocess as that user.
The script must be ran as root.
The user must also exist.

Usage: ./run_as ros2_user
Expected output: ros2_user
"""

import os
import pwd
import subprocess
import sys

from launch_ros_sandbox.descriptions import User


def run_as_user(user: User) -> None:
    """Parse User object and run 'whoami' as that user."""
    pw_record = pwd.getpwuid(user.uid)

    env = os.environ.copy()
    env['HOME'] = pw_record.pw_dir
    env['LOGNAME'] = pw_record.pw_name
    env['USER'] = pw_record.pw_name

    def set_user():
        """Set the current user."""
        os.setgid(user.gid)
        os.setuid(user.uid)

    # This should probably use asyncio, since ExecuteNode uses it internally.
    # asyncio uses Popen internally, so this feature should work on it.

    process = subprocess.Popen(
        ['whoami'],
        preexec_fn=set_user,
        env=env
    )

    assert 0 == process.wait()


if __name__ == '__main__':
    if os.getgid() != 0 or os.getuid() != 0:
        raise Exception('Script must be run as root!')

    username = sys.argv[1]
    run_as_user(User.from_username(username))
