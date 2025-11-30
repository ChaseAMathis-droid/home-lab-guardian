"""Tests for CLI commands"""

import pytest
from click.testing import CliRunner

from hlg.cli import cli, config


def test_cli_version():
    """Test CLI version command"""
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "0.1.0" in result.output


def test_cli_config():
    """Test config command"""
    runner = CliRunner()
    result = runner.invoke(config)
    assert result.exit_code == 0
    assert "Current Configuration" in result.output
    assert "Log Path" in result.output


def test_cli_run_missing_log(tmp_path):
    """Test run command with missing log file"""
    runner = CliRunner()
    result = runner.invoke(cli, ["run", "--log-path", str(tmp_path / "nonexistent.log")])
    assert result.exit_code != 0
    assert "not found" in result.output or "does not exist" in result.output
