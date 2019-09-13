#!/bin/bash

# pull the image now so that we don't have to guess/query when its done in the script
docker pull osrf/ros:dashing-desktop

# run the example; loads listener in Docker
./examples/minimal_sandbox_docker.launch.py&
task_id=$!

echo "TaskID: $task_id"

echo "Checking if sandboxed-listener-node is running..."
docker inspect -f "{{.State.Running}}" sandboxed-listener-node
is_running=$?

# Wait until the docker container is running. docker inspect will return 0 when it does.
while [[ $is_running -ne 0 ]]
do
  sleep 1
  docker inspect -f "{{.State.Running}}" sandboxed-listener-node
  is_running=$?
done

# Run listener in the container spun up by DockerPolicy for 5 seconds
echo "Executing listener in Docker container..."
timeout 5 docker exec -t sandboxed-listener-node /ros_entrypoint.sh ros2 run demo_nodes_cpp listener
echo "Stopping Docker container..."

# Note: these sleep commands are here just so the following command executes after stdout appears on
# the terminal.
kill -INT $task_id
sleep 2

# SIGTERM is required also if launch is ran in the background, this might be a bug in launch.
kill $task_id
sleep 2

echo "Checking if sandboxed-listener-node is running..."
docker inspect -f "{{.State.Running}}" sandboxed-listener-node

# Check the exit code of docker inspect. 0 is returned only if it is running.
# This check will set the exit code to 0 only if the exit code is not 0.
[[ $? -ne 0 ]]

exit $?