# Copyright 2019 Canonical Ltd
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

from pathlib import Path

import pytest


@pytest.mark.mypy
@pytest.mark.linter
def test_mypy():
    # TODO: when ament_mypy is officially released, remove this check and move import to the top
    # of the file. Until then, we still use it internally as developers.
    try:
        from ament_mypy.main import main
        config_path = Path(__file__).parent / 'config' / 'mypy.ini'
        print(config_path.resolve())
        rc = main(argv=['launch_ros_sandbox', '--config', str(config_path.resolve())])
        assert rc == 0, 'Found code style errors / warnings'
    except ImportError:
        pass
