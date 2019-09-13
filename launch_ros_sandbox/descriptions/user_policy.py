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
import pwd
import subprocess
from typing import List
from typing import Optional

import launch
from launch import Action
from launch import LaunchContext
from launch.utilities import perform_substitutions

from launch_ros.substitutions import ExecutableInPackage

from launch_ros_sandbox.actions.load_runas_nodes import LoadRunAsNodes
from launch_ros_sandbox.descriptions.policy import Policy
from launch_ros_sandbox.descriptions.sandboxed_node import SandboxedNode
from launch_ros_sandbox.descriptions.user import User


class UserPolicy(Policy):
    """
    UserPolicy defines parameters for running a sandboxed node as a different user.

    UserPolicy extends Policy. All parameters passed into UserPolicy are immutable and are only
    processed once the SandboxedNodeContainer is executed.
    """

    def __init__(
        self,
        *,
        run_as: Optional[User] = None,
    ) -> None:
        """Construct the UserPolicy."""
        self.__logger = launch.logging.get_logger(__name__)
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

    def apply(
        self,
        context: LaunchContext,
        node_descriptions: List[SandboxedNode]
    ) -> Action:
        """Apply the policy any launches the ROS2 nodes in the sandbox."""
        user = self.run_as
        pw_record = pwd.getpwuid(user.uid)

        env = os.environ.copy()
        env['HOME'] = pw_record.pw_dir
        env['LOGNAME'] = pw_record.pw_name
        env['USER'] = pw_record.pw_name
        self.__logger.debug('Running as: {}'.format(pw_record.pw_name))
        self.__logger.debug('\tuid: {}'.format(user.uid))
        self.__logger.debug('\tgid: {}'.format(user.gid))
        self.__logger.debug('\thome: {}'.format(pw_record.pw_dir))

        def set_user() -> None:
            """Set the current user."""
            os.setgid(user.gid)
            os.setuid(user.uid)

        for description in node_descriptions:
            package_name = perform_substitutions(
                context,
                description.package
            )
            executable_name = perform_substitutions(
                context,
                description.node_executable
            )

            # TODO: support node namespace and node name
            # TODO: support parameters
            # TODO: support remappings

            cmd = [ExecutableInPackage(
                package=package_name,
                executable=executable_name
            ).perform(context)]

            self.__logger.info('Running: {}'.format(cmd))

            subprocess.Popen(
                cmd,
                preexec_fn=set_user,
                env=env
            )

            # TODO: handle events for process

        # TODO: LaunchAsUser is currently NO-OP due to all sandboxing logic being handled here.
        return LoadRunAsNodes()
