"""Tests for plugin.py module."""

import pathlib
from typing import TYPE_CHECKING, Callable, Dict

import pytest

from pdm_pip_index_url.plugin import process_pip_envs

if TYPE_CHECKING:
    from pdm.pytest import PDMCallable

LogCallback = Callable[[str], None]


@pytest.fixture
def log() -> LogCallback:
    """`pdm.termui.UI` replacement."""
    print()
    return print


PIP_INDEX_URL_1_NO_AUTH: str = "https://test.pypi.org/"
PIP_INDEX_URL_2_NO_AUTH: str = "http://test2.pypi.org/"
PIP_INDEX_URL_3_WITH_AUTH: str = "https://john:doe@test3.pypi.org/"
PIP_INDEX_URL_3_NO_AUTH: str = "https://test3.pypi.org/"
PIP_INDEX_URL_3_USERNAME: str = "john"
PIP_INDEX_URL_3_PASSWORD: str = "doe"
PIP_INDEX_URL_4_WITH_AUTH: str = "https://johndoe@test4.pypi.org/"
PIP_INDEX_URL_4_NO_AUTH: str = "https://test4.pypi.org/"
PIP_INDEX_URL_4_USERNAME: str = "foo"
PIP_INDEX_URL_4_PASSWORD: str = "johndoe"


@pytest.mark.parametrize(
    "envs,expected_envs",
    [
        ({}, {}),
        (
            {"PIP_INDEX_URL": PIP_INDEX_URL_1_NO_AUTH},
            {
                "PIP_INDEX_URL": PIP_INDEX_URL_1_NO_AUTH,
                "PDM_PYPI_URL": PIP_INDEX_URL_1_NO_AUTH,
            },
        ),
        (
            {"PIP_EXTRA_INDEX_URL": PIP_INDEX_URL_1_NO_AUTH},
            {
                "PIP_EXTRA_INDEX_URL": PIP_INDEX_URL_1_NO_AUTH,
                "PDM_PYPI_URL": PIP_INDEX_URL_1_NO_AUTH,
            },
        ),
        (
            {
                "PIP_INDEX_URL": PIP_INDEX_URL_1_NO_AUTH,
                "PIP_EXTRA_INDEX_URL": PIP_INDEX_URL_2_NO_AUTH,
            },
            {
                "PIP_INDEX_URL": PIP_INDEX_URL_1_NO_AUTH,
                "PIP_EXTRA_INDEX_URL": PIP_INDEX_URL_2_NO_AUTH,
                "PDM_PYPI_URL": PIP_INDEX_URL_1_NO_AUTH,
            },
        ),
        (
            {
                "PIP_INDEX_URL": PIP_INDEX_URL_1_NO_AUTH,
                "PDM_PYPI_USERNAME": "foo",
            },
            {
                "PIP_INDEX_URL": PIP_INDEX_URL_1_NO_AUTH,
                "PDM_PYPI_USERNAME": "foo",
            },
        ),
        (
            {
                "PIP_INDEX_URL": PIP_INDEX_URL_1_NO_AUTH,
                "PDM_PYPI_PASSWORD": "foo",
            },
            {
                "PIP_INDEX_URL": PIP_INDEX_URL_1_NO_AUTH,
                "PDM_PYPI_PASSWORD": "foo",
            },
        ),
        (
            {
                "PIP_INDEX_URL": PIP_INDEX_URL_1_NO_AUTH,
                "PDM_PYPI_URL": PIP_INDEX_URL_2_NO_AUTH,
            },
            {
                "PIP_INDEX_URL": PIP_INDEX_URL_1_NO_AUTH,
                "PDM_PYPI_URL": PIP_INDEX_URL_2_NO_AUTH,
            },
        ),
        (
            {
                "PIP_INDEX_URL": PIP_INDEX_URL_1_NO_AUTH,
                "PDM_PYPI_URL": PIP_INDEX_URL_2_NO_AUTH,
            },
            {
                "PIP_INDEX_URL": PIP_INDEX_URL_1_NO_AUTH,
                "PDM_PYPI_URL": PIP_INDEX_URL_2_NO_AUTH,
            },
        ),
        (
            {
                "PIP_INDEX_URL": PIP_INDEX_URL_3_WITH_AUTH,
            },
            {
                "PIP_INDEX_URL": PIP_INDEX_URL_3_WITH_AUTH,
                "PDM_PYPI_URL": PIP_INDEX_URL_3_NO_AUTH,
                "PDM_PYPI_USERNAME": PIP_INDEX_URL_3_USERNAME,
                "PDM_PYPI_PASSWORD": PIP_INDEX_URL_3_PASSWORD,
            },
        ),
        (
            {
                "PIP_INDEX_URL": PIP_INDEX_URL_4_WITH_AUTH,
            },
            {
                "PIP_INDEX_URL": PIP_INDEX_URL_4_WITH_AUTH,
                "PDM_PYPI_URL": PIP_INDEX_URL_4_NO_AUTH,
                "PDM_PYPI_USERNAME": PIP_INDEX_URL_4_USERNAME,
                "PDM_PYPI_PASSWORD": PIP_INDEX_URL_4_PASSWORD,
            },
        ),
    ],
)
def test_process_pip_envs(
    envs: Dict[str, str], expected_envs: Dict[str, str], log: LogCallback
) -> None:
    """Check if envs are processed as expected."""
    process_pip_envs(envs=envs, log=log)
    assert envs == expected_envs


def test_pdm_usage(pdm: "PDMCallable", tmp_path: pathlib.Path) -> None:
    """Run pdm within current environment to check if plugin actually works.

    NOTE: This test requires this project to be installed via `pdm install`.
    """
    output_file: pathlib.Path = tmp_path / "output.txt"
    expected_url: str = "foo.com"
    pdm(
        [
            "run",
            "-v",
            "python",
            "-c",
            "import os;"
            f"fh = open(r'{output_file!s}', 'w');"
            "fh.write(str(os.environ.get('PDM_PYPI_URL')));"
            "fh.close()",
        ],
        env={"PIP_INDEX_URL": expected_url},
        strict=True,
    )
    assert output_file.read_text(encoding="utf-8").strip() == expected_url
