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

"""Module for UserPolicy."""

import os

from typing import Optional

from launch_ros_sandbox.descriptions import User


class UserPolicy:
    """UserPolicy defines parameters for running a sandboxed node as a different user."""

    def __init__(
        self,
        *,
        run_as: Optional[User] = None,
    ) -> None:
        """Construct the UserPolicy."""
        # default to current user if `run_as` is undefined.
        if run_as is not None:
            self._run_as = run_as
        else:
            self._run_as = User(
                uid=os.getuid(),
                gid=os.getgid())

    @property
    def run_as(self) -> User:
        """Get the User to run as."""
        return self._run_as
