
# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Module for the Docker Image description."""

import logging

import docker
from docker.models.images import Image
from docker.errors import APIError, ImageNotFound


class DockerImage(object):
    """A Docker Image consists of a repository and tag."""

    def __init__(
        self,
        repository: str = None,
        tag: str = None
    ):
        """Construct the DockerImage description."""
        # Pass repository and tag or just image_id
        if repository is None:
            raise TypeError("You must specify at least the repository.")
        self._repository = repository
        self._tag = 'latest' if tag is None else tag
        self._docker_client = docker.from_env()
        self._docker_image = None

    @property
    def repository(self) -> str:
        """Get the Docker image repository."""
        return self._repository

    @property
    def tag(self) -> str:
        """Get the Docker image tag."""
        return self._tag

    @property
    def docker_image(self) -> Image:
        """Return an Docker Image object."""
        return self._docker_image

    @property
    def docker_client(self) -> docker.DockerClient:
        """Return an instance of the Docker client."""
        return self._docker_client
