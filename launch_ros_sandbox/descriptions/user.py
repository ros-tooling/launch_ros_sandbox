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

"""Module for User."""

import pwd


class User:
    """User is a pair of Unix UID and GID."""

    def __init__(
        self,
        *,
        uid: int,
        gid: int
    ) -> None:
        """Construct the User."""
        self._uid = uid
        self._gid = gid

    @classmethod
    def from_username(cls, username: str) -> 'User':
        """Get a User object from a username string."""
        user = pwd.getpwnam(username)

        return cls(
            uid=user.pw_uid,
            gid=user.pw_gid)

    @property
    def uid(self) -> int:
        """Get the User's user id."""
        return self._uid

    @property
    def gid(self) -> int:
        """Get the User's group id."""
        return self._gid
