# ROS 2 Launch Sandbox
ROS 2 launch Sandbox is an extension of Launch that adds sandboxing capabilities to ROS 2 Launch.

ROS 2 Launch Sandbox delegates LaunchDescription parameters to a sandboxed ROS 2 Launch which then can run ROS 2 nodes in a secure environment.

## Installing
``` bash
$ python3 setup.py install --user
```

## Testing
The initialization of SandboxedNodeContainer can be tested by first installing the project as a Python package and then running examples/minimal_sandboxed_node_container.py

``` bash
$ ./examples/minimal_sandboxed_node_container.py
```
