FROM osrf/ros:dashing-desktop

# copy the python package 
COPY . /opt/launch_ros_sandbox

# set shell to bash
SHELL ["/bin/bash", "-c"]

# compile and install the python package (as root)
RUN source /opt/ros/dashing/setup.bash && \
  cd /opt/launch_ros_sandbox && \
  python3 setup.py install --user

# create sandboxed ros user and execute "./examples/run_as.py" with that user.
# the build will fail if run_as does not work.
RUN useradd -m dashing && \
  source /opt/ros/dashing/setup.bash && \
  cd /opt/launch_ros_sandbox && \
  ./examples/run_as.py dashing

WORKDIR /opt/launch_ros_sandbox