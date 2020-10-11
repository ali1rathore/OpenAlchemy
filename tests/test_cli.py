"""Tests for the CLI."""

import os
import pathlib
import sys
from unittest import mock

import pytest

from open_alchemy import cli
from open_alchemy import exceptions
from open_alchemy import helpers


@pytest.mark.parametrize(
    "specfile",
    [
        pytest.param("spec.json", id="valid json specfile"),
        pytest.param("spec.yml", id="valid yml specfile"),
        pytest.param("spec.yaml", id="valid yaml specfile"),
    ],
)
@pytest.mark.cli
def test_validate_specfile_valid(tmp_path, specfile):
    """
    GIVEN a valid specification file
    WHEN validate_specfile is called
    THEN nothing happens
    """
    spec = tmp_path / specfile
    spec.write_text("")

    cli.validate_specfile(spec)


@pytest.mark.cli
def test_validate_specfile_invalid_extension(tmp_path):
    """
    GIVEN a invalid specification file extension
    WHEN validate_specfile is called
    THEN a ValueError exception is raised
    """
    spec = tmp_path / "specfile.txt"
    spec.write_text("")

    with pytest.raises(exceptions.CLIError):
        cli.validate_specfile(spec)


@pytest.mark.cli
def test_validate_specfile_does_not_exist(tmp_path):
    """
    GIVEN a specification file which does not exist
    WHEN validate_specfile is called
    THEN a ValueError exception is raised
    """
    spec = tmp_path / "specfile.txt"

    with pytest.raises(exceptions.CLIError):
        cli.validate_specfile(spec)


@pytest.mark.parametrize(
    "command, expected_arguments",
    [
        pytest.param(
            ["openalchemy", "build", "my_specfile", "my_package", "my_output_dir"],
            ["specfile='my_specfile'", "name='my_package'", "output='my_output_dir'"],
            id="cli help command",
        ),
    ],
)
@pytest.mark.cli
def test_build_application_parser(command, expected_arguments):
    """
    GIVEN an argument on the command line
    WHEN the application parser is built
    THEN arguments are returned
    """
    sys.argv = command

    args = cli.build_application_parser()

    str_args = str(args)
    for expected_argument in expected_arguments:
        assert expected_argument in str_args


@pytest.mark.cli
def test_build(mocker):
    """
    GIVEN arguments from the parser
    WHEN they are passed to the build() function
    THEN the function execute
    """
    m_validate = mocker.patch("open_alchemy.cli.validate_specfile")
    m_build_json = mocker.patch("open_alchemy.cli.build_json")
    args = mock.MagicMock()
    args.specfile = pathlib.Path("spec.json")

    cli.build(args)

    m_validate.assert_called_once()
    m_build_json.assert_called_once()


@pytest.mark.parametrize(
    "command, expected_file",
    [
        pytest.param(
            f"build {pathlib.Path.cwd() / 'examples' / 'simple' / 'example-spec.yml'}"
            " simple .",
            "simple/setup.py",
            id="cli build all",
        ),
    ],
)
@pytest.mark.cli
def test_main(tmp_path, _remember_current_directory, command, expected_file):
    """
    GIVEN CLI options are set
    WHEN the CLI is called
    THEN the program runs
    """
    os.chdir(tmp_path)
    sys.argv = ["openalchemy"] + command.split()

    cli.main()

    assert pathlib.Path(expected_file).exists()


@pytest.mark.cli
def test_invalid_main(tmp_path, _remember_current_directory):
    """
    GIVEN an invalid CLI command is used
    WHEN the CLI is called
    THEN the program fails and the error is logged
    """
    os.chdir(tmp_path)
    sys.argv = ["openalchemy", "build", "my_specfile", "my_package", "my_output_dir"]

    cli.main()


@pytest.mark.cli
def test_external_cli():
    """
    GIVEN
    WHEN we run the CLI as an external command
    THEN nothing fails
    """
    out, _ = helpers.command.run(["openalchemy", "--help"], str(pathlib.Path.cwd()))

    assert "usage: openalchemy" in out
