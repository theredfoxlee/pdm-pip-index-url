"""Tests for plugin.py module."""

from typing import Callable, Final

import pytest

from pdm_pip_index_url.plugin import process_pip_envs

LogCallback = Callable[[str], None]


@pytest.fixture
def log() -> LogCallback:
    """`pdm.termui.UI` replacement."""
    print()
    return print


PIP_INDEX_URL_1_NO_AUTH: Final[str] = "https://test.pypi.org/"
PIP_INDEX_URL_2_NO_AUTH: Final[str] = "http://test2.pypi.org/"
PIP_INDEX_URL_3_WITH_AUTH: Final[str] = "https://john:doe@test3.pypi.org/"
PIP_INDEX_URL_3_NO_AUTH: Final[str] = "https://test3.pypi.org/"
PIP_INDEX_URL_3_USERNAME: Final[str] = "john"
PIP_INDEX_URL_3_PASSWORD: Final[str] = "doe"
PIP_INDEX_URL_4_WITH_AUTH: Final[str] = "https://johndoe@test4.pypi.org/"
PIP_INDEX_URL_4_NO_AUTH: Final[str] = "https://test4.pypi.org/"
PIP_INDEX_URL_4_USERNAME: Final[str] = "foo"
PIP_INDEX_URL_4_PASSWORD: Final[str] = "johndoe"


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
    envs: dict[str, str], expected_envs: dict[str, str], log: LogCallback
) -> None:
    """Check if envs are processed as expected."""
    process_pip_envs(envs=envs, log=log)
    assert envs == expected_envs
