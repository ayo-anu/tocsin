"""Smoke tests for the initial command-line entry point."""

from pytest import CaptureFixture

from tocsin.cli import main


def test_main_prints_placeholder(capsys: CaptureFixture[str]) -> None:
    """The entry point emits its documented deterministic output."""
    assert main() == 0
    assert capsys.readouterr().out == "Tocsin project initialized.\n"
