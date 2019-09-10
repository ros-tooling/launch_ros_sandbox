# ROS2 Launch Sandbox
ROS2 Launch Sandbox is an extension of Launch that adds sandboxing capabilities to ROS2 Launch.

ROS2 Launch Sandbox delegates LaunchDescription parameters to a sandboxed environment which will run ROS 2 nodes.

Different sandboxing 'policies' can be applied to determine how you would like to execute nodes.

The policies currently supported are:

1. `UserPolicy`: Run ROS2 nodes as a specific user.
2. `DockerPolicy`: Run ROS2 nodes in a Docker container.

## Installing

Install the project as a python package.

``` bash
$ python3 setup.py install --user
```

## Usage

A working example is provided in [`examples/minimal_sandboxed_node_container.launch.py`](examples/minimal_sandboxed_node_container.launch.py).

``` bash
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
