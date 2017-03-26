import json
import subprocess

import pytest

from tests.conftest import create_runner, strip_output


@pytest.fixture(scope='session')
def runner(tmpdir_factory, image_path, request, config_path):
    runner = create_runner(tmpdir_factory, request, config_path)

    scenario = {
        "scenario": "acceptance_boot",
        "cnt_nodes": 1,
        "provisioning": {
            "image": image_path,
            "regex_shell_prompt": "root@OpenWrt:/#"
        }
    }

    with runner() as r:
        yield r, scenario


@pytest.fixture
def snapshot_runner(runner):
    runner, scenario = runner
    runner.start_scenario(scenario)
    yield runner
    runner.stop(hard=False)


def test_info_scenario(snapshot_runner):
    res = subprocess.check_output(['./mw.py', 'info', 'scenario'])
    with open(snapshot_runner.scenario, 'r') as f:
        assert strip_output(res) == json.dumps(json.load(f), indent=4)


def test_ping(snapshot_runner):
    res = subprocess.check_output(['./mw.py', 'ping'])
    assert strip_output(res) == 'pong'