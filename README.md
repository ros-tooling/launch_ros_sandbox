# launch-ros-sandbox

A sandboxing plugin for launch_ros

[Link to documentation](https://launch-ros-sandbox.readthedocs.io)

## Installing

Install the project as a python package:

```bash
$ python3 setup.py install --user
```

Check that your user is in the Docker user group:

```bash
$ groups
```

If you dont see `docker`, then add your user to the Docker group:

```bash
$ sudo usermod -aG docker $USER
```

## Usage

A working example is provided in [examples/minimal_sandboxed_node_container.launch.py](https://github.com/aws-robotics/launch-ros-sandbox/tree/master/examples/minimal_sandboxed_node_container.launch.py).

```bash
$ ./examples/minimal_sandboxed_node_container.py
```

Creating a sandboxed node is very similar to creating a regular launch file.

Add a `SandboxedNodeContainer()` action like you would with a regular launch file, but make sure to provide the `sandbox_name` and `policy`.
Adding nodes is also similar to regular launch files, however, you should use `launch_ros_sandbox.descriptions.SandboxedNode()` instead.

A launch file with nodes running as a certain user would look like:

```python
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
```

## License

This library is licensed under the Apache 2.0 License.


## Build Status

This stack supports the following ROS 2 releases:

 * Dashing

| ROS 2 Release | Development  | Source Debian Package | X86-64 Debian Package | ARM64 Debian Package | ARMHF Debian package |
| ------------- | ------------ | --------------------- | --------------------- | -------------------- | -------------------- |
| Dashing       | [![Build Status](http://build.ros2.org/buildStatus/icon?job=Ddev__launch_ros_sandbox__ubuntu_bionic_amd64)](http://build.ros2.org/job/Ddev__launch_ros_sandbox__ubuntu_bionic_amd64) | [![Build Status](http://build.ros2.org/buildStatus/icon?job=Dsrc_uB__launch_ros_sandbox__ubuntu_bionic__source)](http://build.ros2.org/job/Dsrc_uB__launch_ros_sandbox__ubuntu_bionic__source) | [![Build Status](http://build.ros2.org/buildStatus/icon?job=Dbin_uB64__launch_ros_sandbox__ubuntu_bionic_amd64__binary)](http://build.ros2.org/job/Dbin_uB64__launch_ros_sandbox__ubuntu_bionic_amd64__binary) | N/A | N/A |
