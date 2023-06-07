import functools
import os
from typing import Callable, MutableMapping

from pdm.core import Core
from pdm.project import Config, Project
from pdm.signals import pre_invoke
from pdm.termui import Verbosity

from .utils import ParsedUrl, find_env, parse_url


def run_plugin(
    environ: MutableMapping[str, str], *, log_detail: Callable[[str], None]
) -> None:
    """Set PDM_PYPI_URL in `environ`."""
    known_pdm_envs: set[str] = {
        "PDM_PYPI_URL",
        "PDM_PYPI_USERNAME",
        "PDM_PYPI_PASSWORD",
    } & environ.keys()

    if known_pdm_envs:
        log_detail(
            "Pip index url search skipped as the following"
            f" envs are already set: {known_pdm_envs}"
        )
        return

    keys: list[str] = ["PIP_INDEX_URL", "PIP_EXTRA_INDEX_URL"]
    log_detail(f"Search for pip index url [{keys=}]")

    if (env := find_env(envs=environ, keys=keys)) is None:
        log_detail("Pip index url was not found")
        return

    log_detail(f"Pip index url was found [source={env[0]}]")
    parsed_url: ParsedUrl = parse_url(url=env[1])

    def verbose_setenv(key: str, value: str) -> None:
        log_detail(f"Setting environment variable: {key}")
        environ[key] = value

    verbose_setenv("PDM_PYPI_URL", parsed_url.url)
    if parsed_url.auth is None:
        return
    verbose_setenv("PDM_PYPI_USERNAME", parsed_url.auth.username)
    verbose_setenv("PDM_PYPI_PASSWORD", parsed_url.auth.password)


def register_plugin(_: Core) -> None:
    def _run_plugin(project: Project, _: Config) -> None:
        run_plugin(
            environ=os.environ,
            log_detail=functools.partial(
                project.core.ui.echo, verbosity=Verbosity.DETAIL
            ),
        )

    pre_invoke.connect(_run_plugin)
