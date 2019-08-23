# Copyright FIXME

""" 
Launch extension for running ROS nodes in a sandboxed environment.

launch_ros_sandbox defines Launch actions to delegate the launch of nodes
to a sandboxed environment.
"""

from launch_ros_sandbox import actions
from launch_ros_sandbox import descriptions

__all__ = [
    'actions',
    'descriptions'
]