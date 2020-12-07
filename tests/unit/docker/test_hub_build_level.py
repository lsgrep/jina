import os

import pytest

from pathlib import Path
from jina.docker.hubio import HubIO
from jina.helper import yaml
from jina.enums import BuildTestLevel
from jina.peapods import Pod
from jina.executors import BaseExecutor
from jina.parser import set_hub_build_parser

cur_dir = Path.cwd()

@pytest.mark.parametrize("test_level, expected_failed_levels", [('FLOW', [BuildTestLevel.EXECUTOR, BuildTestLevel.POD_NONDOCKER, BuildTestLevel.FLOW]),
('EXECUTOR', [BuildTestLevel.EXECUTOR]),
('POD_DOCKER', [BuildTestLevel.EXECUTOR, BuildTestLevel.POD_NONDOCKER]),
('POD_NONDOCKER', [BuildTestLevel.EXECUTOR, BuildTestLevel.POD_NONDOCKER])])
def test_hub_build_pull(test_level, expected_failed_levels):
    args = set_hub_build_parser().parse_args([os.path.join(cur_dir, 'hub-mwu'), '--push', '--host-info', '--test-level', test_level])
    p_names, failed_levels = HubIO(args)._test_build("jinahub/pod.dummy_mwu_encoder")

    assert expected_failed_levels == failed_levels
