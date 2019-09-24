#!/bin/bash

# Launch a container with container name 'sandboxed-listener-node'

# Retrieve the available CPUs for the Docker container's cgroup
docker exec sandboxed-listener-node cat /sys/fs/cgroup/cpuset/cpuset.cpus
