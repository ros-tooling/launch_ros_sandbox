#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
NORM='\033[0m'

# pull the image now so that we don't have to guess/query when its done in the script
docker pull osrf/ros:dashing-desktop

# run the example; loads listener in Docker
./examples/mem_limit_sandbox_docker.launch.py&
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
echo "Checking memory limits in Docker container..."
memory=$(docker inspect sandboxed-listener-node | jq '.[0].HostConfig.Memory')
if [[ "$memory" -eq "134217728" ]]; then
    printf "${GREEN}PASS: Memory limits correctly set to 128m!${NORM}\n";
    result=0
else
    printf "${RED}FAIL: Memory limits not correctly set to 128m!${NORM}\n";
    result=1
fi

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
# This check will set the exit code to 0 only if the Docker container is not running and the memory check passed.
[[ $? -ne 0 && result -eq 0 ]]

exit $?