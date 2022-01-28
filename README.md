# DEPRECATED package

This package is no longer under development. It was built for a 2019 Roscon workshop and has no future planned usage or maintenance. Repository not deleted for historical reasons (so as not to break existing indexes that contain links to it)

# launch_ros_sandbox

![License](https://img.shields.io/github/license/ros-security/launch_ros_sandbox)
[![Documentation Status](https://readthedocs.org/projects/launch_ros_sandbox/badge/?version=latest)](https://launch_ros_sandbox.readthedocs.io/en/latest/?badge=latest)

`launch_ros_sandbox` is a `roslaunch2` extension.

Using `launch_ros_sandbox`, you can define launch files running nodes in
restrained environments, such as Docker containers or separate user accounts
with limited privileges.

[Package documentation][launch_ros_sandbox_doc]

## Installing

### Prerequisites

`launch_ros_sandbox` requires Docker to be installed on your machine and that
your user can execute `docker` commands.

Check that your current user account is a member of the `docker` group:

```bash
groups | grep docker
```

If `docker` is not listed, add yourself to the group using:

```bash
sudo usermod -aG docker $USER
```

### Binary Packages

#### Dashing

On Ubuntu 18.04, you can install `launch_ros_sandbox` by running:

```sh
sudo apt install ros-dashing-launch-ros-sandbox
```

### Installing from source

#### Dashing (`dashing-devel` branch)

This is the recommended way to install this software.

* Install ROS 2 Dashing on your machine following the
  [official instructions][ros2_dashing_setup]. We recommend you use the
  official binary packages for your platform, if available.
* Checkout the code source and compile it as follow:

```bash
# If you use bash or zsh, source setup.bash or setup.zsh, instead of setup.sh
source /opt/ros/dashing/setup.sh
mkdir -p ~/ros2_dashing_ros_launch_sandbox_ws/src
cd ros2_dashing_ros_launch_sandbox_ws
# Clone this package repository using vcs.
curl https://raw.githubusercontent.com/ros-security/launch_ros_sandbox/master/launch_ros_sandbox.dashing.repos | vcs import src/
# Install all required system dependencies
rosdep update
rosdep install --ignore-packages-from-source --from-paths src/
# Use colcon to compile launch_ros_sandbox code and all its dependencies
colcon build --packages-up-to launch_ros_sandbox
```

#### Latest (unstable development - `master` branch)

Please follow those instructions if you plan to contribute to this repository.

* Install all software dependencies required for ROS 2 development by
  following the [ROS 2 documentation][ros2_latest_setup].
* Checkout the code source and compile it as follow:

```bash
mkdir -p ~/ros2_latest_ros_launch_sandbox_ws/src
cd ros2_latest_ros_launch_sandbox_ws
# Use vcs to clone all required repositories
curl https://raw.githubusercontent.com/ros2/ros2/dashing/ros2.repos | vcs import src/
curl https://raw.githubusercontent.com/ros-security/launch_ros_sandbox/master/launch_ros_sandbox.repos | vcs import src/
# Install all required system dependencies
# Some packages may fail to install, this is expected on an unstable branch,
# and is generally OK.
rosdep update
rosdep install -r --rosdistro=eloquent --ignore-packages-from-source --from-paths src/
# Use colcon to compile launch_ros_sandbox code and all its dependencies
colcon build --packages-up-to launch_ros_sandbox
```

## Usage

A working example is provided in
[examples/minimal_sandboxed_node_container.launch.py][ex_minimal_sandboxed_node_container_launch]

```bash
./examples/minimal_sandboxed_node_container.py
```

Creating a sandboxed node is very similar to creating a regular launch file.

Add a `SandboxedNodeContainer()` action like you would with a regular launch
file, but make sure to provide the `sandbox_name` and `policy`.
Adding nodes is also similar to regular launch files, however, you should use
`launch_ros_sandbox.descriptions.SandboxedNode()` instead.

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

| ROS 2 Release | Branch Name     | Development | Source Debian Package | X86-64 Debian Package | ARM64 Debian Package | ARMHF Debian package |
| ------------- | --------------- | ----------- | --------------------- | --------------------- | -------------------- | -------------------- |
| Latest        | `master`        | [![Test Pipeline Status](https://github.com/ros-security/launch_ros_sandbox/workflows/Test%20launch_ros_sandbox/badge.svg)](https://github.com/ros-security/launch_ros_sandbox/actions) | N/A                   | N/A                   | N/A                  | N/A                  |
| Dashing       | `dashing-devel` | [![Build Status](http://build.ros2.org/buildStatus/icon?job=Ddev__launch_ros_sandbox__ubuntu_bionic_amd64)](http://build.ros2.org/job/Ddev__launch_ros_sandbox__ubuntu_bionic_amd64) | [![Build Status](http://build.ros2.org/buildStatus/icon?job=Dsrc_uB__launch_ros_sandbox__ubuntu_bionic__source)](http://build.ros2.org/job/Dsrc_uB__launch_ros_sandbox__ubuntu_bionic__source) | [![Build Status](http://build.ros2.org/buildStatus/icon?job=Dbin_uB64__launch_ros_sandbox__ubuntu_bionic_amd64__binary)](http://build.ros2.org/job/Dbin_uB64__launch_ros_sandbox__ubuntu_bionic_amd64__binary) | N/A | N/A |

[ex_minimal_sandboxed_node_container_launch]: examples/minimal_sandboxed_node_container.launch.py
[launch_ros_sandbox_doc]: https://launch_ros_sandbox.readthedocs.io
[ros2_dashing_setup]: https://index.ros.org/doc/ros2/Installation/Dashing/
[ros2_latest_setup]: https://index.ros.org/doc/ros2/Installation/Latest-Development-Setup/
