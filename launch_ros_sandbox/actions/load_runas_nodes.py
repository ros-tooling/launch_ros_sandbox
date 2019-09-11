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


"""
Internal module for the LoadRunAsNodes Action.

LoadRunAsNodes is an Action that controls the lifecycle of a sandboxed environment running nodes as
a separate user. This Action is not exported and should only be used internally.
"""

from launch import Action


class LoadRunAsNodes(Action):
    """
    LoadRunAsNodes is an Action that controls the sandbox environment spawned by `UserPolicy`.

    LoadRunAsNodes should only be constructed by `UserPolicy.apply`.
    FIXME: Move the logic for launching the sandbox environment into `LoadRunAsNodes.execute`
    """

    pass
