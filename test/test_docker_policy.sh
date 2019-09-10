#!/bin/bash

./examples/minimal_sandbox_docker.py
docker ps

echo "Executing listener in Docker container..."
timeout 5 docker exec -t sandboxed-listener-node /ros_entrypoint.sh ros2 run demo_nodes_cpp listener
echo "Stopping Docker container..."
docker stop sandboxed-listener-node
