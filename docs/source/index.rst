.. launch-ros-sandbox documentation master file, created by
   sphinx-quickstart on Thu Sep 19 08:53:28 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

launch-ros-sandbox
==================

A sandboxing plugin for `launch_ros <https://github.com/ros2/launch_ros>`_

ROS2 Launch Sandbox is an extension of Launch that adds sandboxing capabilities to ROS2 Launch.

ROS2 Launch Sandbox delegates LaunchDescription parameters to a sandboxed environment which will run ROS 2 nodes.

Different sandboxing 'policies' can be applied to determine how you would like to execute nodes.

The policies currently supported are:

1. :code:`UserPolicy`: Run ROS2 nodes as a specific user.
2. :code:`DockerPolicy`: Run ROS2 nodes in a Docker container.

Installing
----------

Install the project as a python package:

.. code-block:: bash

   $ python3 setup.py install --user

Check that your user is in the Docker user group:

.. code-block:: bash
	
   $ groups

If you dont see :code:`docker`, then add your user to the Docker group:

.. code-block:: bash
	
   $ sudo usermod -aG docker $USER

Usage
-----

A working example is provided in `examples/minimal_sandboxed_node_container.launch.py <https://github.com/aws-robotics/launch-ros-sandbox/tree/master/examples/minimal_sandboxed_node_container.launch.py>`_.

.. code-block::  bash
	
   $ ./examples/minimal_sandboxed_node_container.py


Creating a sandboxed node is very similar to creating a regular launch file.

Add a :code:`SandboxedNodeContainer()` action like you would with a regular launch file, but make sure to provide the :code:`sandbox_name` and :code:`policy`.
Adding nodes is also similar to regular launch files, however, you should use :code:`launch_ros_sandbox.descriptions.SandboxedNode()` instead.

A launch file with nodes running as a certain user would look like:

.. code-block:: python

   def generate_launch_description() -> launch.LaunchDescription:
      ld = launch.LaunchDescription()

      ld.add_action(
        	launch_ros_sandbox.actions.SandboxedNodeContainer(
            	sandbox_name='my_sandbox',
            	policy=UserPolicy(run_as=User.from_username('dashing')),
            	node_descriptions=[
            		launch_ros_sandbox.descriptions.SandboxedNode(
                    	package='demo_nodes_cpp', node_executable='talker'),
                	launch_ros_sandbox.descriptions.SandboxedNode(
                    	package='demo_nodes_cpp', node_executable='listener')
            	]
        	)
    	)


License
-------

This library is licensed under the Apache 2.0 License.

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   modules
   actions
   descriptions