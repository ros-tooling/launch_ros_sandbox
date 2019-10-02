#!/bin/bash

echo "Running './examples/bad_image.launch.py'"

output=$(timeout -s INT 10s ./examples/bad_image.launch.py)

if [[ $? -ne 0 ]]
then
    echo "The example script did not exit automatically."
    exit 3
fi

if [[ $output == *"[WARNING] [launch_ros_sandbox.actions.load_docker_nodes]: 404 Client Error: Not Found"* ]]
then
    echo "The bad image was not found on DockerHub"
else
    echo "The bad image was found. Either someone created it on DockerHub and the test needs to be fixed or the the test failed."
    exit 1
fi

if [[ $output == *"[ERROR] [launch_ros_sandbox.actions.load_docker_nodes]: 404 Client Error: Not Found"* ]]
then
    echo "The bad image could not be ran as a container. The test passed."
else
    echo "The bad image was able to run. Either it exists locally and the test needs to be fixed or the test failed."
    exit 2
fi

exit 0
