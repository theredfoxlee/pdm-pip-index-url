import os
from typing import Mapping, NamedTuple, Optional

from pdm.core import Core
from pdm.project import Config, Project
from pdm.signals import pre_invoke
from pdm.termui import Verbosity


def get_pip_index_url(env: Mapping[str, str]) -> Optional[str]:
    """Return value of either PIP_INDEX_URL or PIP_EXTRA_INDEX_URL (when defined)."""
    return env.get("PIP_INDEX_URL", env.get("PIP_EXTRA_INDEX_URL"))


def raise_for_invalid_env(env: Mapping[str, str]) -> None:
    if (
        set_envs := {"PDM_PYPI_URL", "PDM_PYPI_USERNAME", "PDM_PYPI_PASSWORD"}
        & env.keys()
    ):
        raise ValueError(f"Environment variables already set: {set_envs}")


class BaseAuth(NamedTuple):
    username: str
    password: str


class PDMConfig(NamedTuple):
    pdm_pypi_url: str
    pdm_pypi_auth: Optional[BaseAuth]


def get_pdm_config(pip_index_url: str) -> PDMConfig:
    # TODO: Better read.
    return PDMConfig(pdm_pypi_url=pip_index_url, pdm_pypi_auth=None)


def plugin_main(project: Project, _: Config) -> None:
    try:
        raise_for_invalid_env(os.environ)
    except ValueError as e:
        project.core.ui.echo(f"Environment validation failed: {e} (skipping)", err=True)
        return

    if (pip_index_url := get_pip_index_url(os.environ)) is None:
        project.core.ui.echo(
            "No PIP_INDEX_URL found (skipping)", verbosity=Verbosity.DETAIL
        )
        return

    pdm_config: PDMConfig = get_pdm_config(pip_index_url=pip_index_url)

    def _verbose_set_env(key: str, value: str) -> None:
        project.core.ui.echo(
            f"Setting env: {key=} (overwrite={key in os.environ})",
            verbosity=Verbosity.DETAIL,
        )
        os.environ[key] = value

    _verbose_set_env("PDM_PYPI_URL", pdm_config.pdm_pypi_url)

    if pdm_config.pdm_pypi_auth is None:
        project.core.ui.echo(
            "No auth found in PIP_INDEX_URL", verbosity=Verbosity.DETAIL
        )
        return

    _verbose_set_env("PDM_PYPI_USERNAME", pdm_config.pdm_pypi_auth.username)
    _verbose_set_env("PDM_PYPI_PASSWORD", pdm_config.pdm_pypi_auth.password)


def register_plugin(_: Core) -> None:
    pre_invoke.connect(plugin_main)
