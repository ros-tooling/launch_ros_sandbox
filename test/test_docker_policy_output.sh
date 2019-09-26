#!/bin/bash

echo "Running './examples/talker_listener_sandbox_docker.launch.py' for 10 seconds"

output=$(timeout -s INT 10s ./examples/talker_listener_sandbox_docker.launch.py)

if [[ $output == *"[talker]: Publishing: 'Hello World:"* ]]
then
    echo "Talker was heard!"
else
    echo "Talker did not output to stdout in the allocated time period."
    exit 1
fi

if [[ $output == *"[listener]: I heard: [Hello World:"* ]]
then
    echo "Listener was heard!"
else
    echo "Listener did not output to stdout in the allocated time period."
    exit 2
fi

exit 0
