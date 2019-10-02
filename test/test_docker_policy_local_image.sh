#!/bin/bash

# pull the image now so that we don't have to guess/query when its done in the script
docker build -t ros-dashing-dummy -f test/dummy-dashing.Dockerfile .

echo "Running './examples/local_image.launch.py' for 10 seconds"

output=$(timeout -s INT 10s ./examples/local_image.launch.py)

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

docker rmi ros-dashing-dummy:latest

exit 0
