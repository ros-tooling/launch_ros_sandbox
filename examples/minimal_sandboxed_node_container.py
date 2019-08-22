#!/usr/bin/env python3

# Copyright FIXME

"""
    Minimal example for using SandboxedNodeContainer

    This example runs a ROS 2 node in a sandboxed environment by invoking SandboxedNodeContainer action.
    SandboxedNodeContainer delegates the launch parameters to an instance of launch_ros that is running in
    a sandboxed environment using the requested sandboxing policy.
    """

import sys

import launch
import launch_ros_sandbox

def generate_launch_description():
    """
    Create launch description for starting SandboxedNodeContainer
    """

    ld = launch.LaunchDescription()

    ld.add_action(
        launch_ros_sandbox.actions.SandboxedNodeContainer(

        )
    )

    print("OK!")

    return ld

if __name__ == "__main__":
    """
    Starts the SandboxedNodeContainer example as a script.
    """

    ls = launch.LaunchService(argv=sys.argv[1:])
    ls.include_launch_description(generate_launch_description())
    sys.exit(ls.run())
