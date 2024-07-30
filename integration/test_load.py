import pytest
from click.testing import CliRunner

from dundie.cli import load, main

from .constants import PEOPLE_FILE

cmd = CliRunner()


@pytest.mark.integration
@pytest.mark.medium
def test_load():
    """test command load"""
    out = cmd.invoke(load, PEOPLE_FILE)
    assert "Dunder Mifflin Associates" in out


@pytest.mark.integration
@pytest.mark.medium
@pytest.mark.parametrize("wrong_command", ["loady", "carrega", "start"])
def test_load_negative_call_load_comand_with_wrong_params(wrong_command):
    """test command load"""
    cmd.invoke(main, wrong_command, PEOPLE_FILE)
    assert out.exit_code != 0
    assert f"No such command '{wrong_command}'," in out.output
