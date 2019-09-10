#!/bin/bash

# FIXME: launch script should hang until all subprocesses complete. This is currently not the case for DockerPolicy
# due to the signal listeners being implemented yet for DockerPolicy.
# Once this is implemented, the following command should be ran as its own process. The cleanup code should also
# be changed to use `kill` instead of `docker stop`. The example could also drop the dependency of knowing the
# container name.
./examples/minimal_sandbox_docker.launch.py
docker ps

echo "Executing listener in Docker container..."
timeout 5 docker exec -t sandboxed-listener-node /ros_entrypoint.sh ros2 run demo_nodes_cpp listener
echo "Stopping Docker container..."

# FIXME: this cleanup line should be replaced with a kill signal once SIGINT is handled by DockerPolicy.
docker stop sandboxed-listener-node
