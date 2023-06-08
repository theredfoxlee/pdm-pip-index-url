"""A module with plugin's business logic."""

import functools
import os
from typing import Any, Callable, MutableMapping

from pdm.core import Core
from pdm.project import Project
from pdm.signals import pre_invoke
from pdm.termui import Verbosity

from .utils import StrippedUrl, find_env, strip_url


def process_pip_envs(
    envs: MutableMapping[str, str], *, log: Callable[[str], None]
) -> None:
    """Mutate `envs` by settings PDM_PYPI_* keys when PIP_* keys are present.

    Processing begins with validating the environment variables. If any PDM_PYPI
    variables are present, processing stops. Otherwise, the script searches for
    PIP_INDEX_URL (or PIP_EXTRA_INDEX_URL if the former is not present). If found,
    any basic auth present in the URL is removed and passed to PDM_PYPI_USERNAME
    and PDM_PYPI_PASSWORD. The stripped URL is set as PDM_PYPI_URL.

    Note that when only `<schema>://<key>@<other>` is passed instead of
    `<schema>://<username>:<password>@<other>`, then the username is set as "foo"
    and the password as `<key>`.
    """
    # [1] Validate environment.
    known_pdm_envs: set[str] = {
        "PDM_PYPI_URL",
        "PDM_PYPI_USERNAME",
        "PDM_PYPI_PASSWORD",
    } & envs.keys()
    if known_pdm_envs:
        log(
            "Pip index url search skipped as the following"
            f" envs are already set: {known_pdm_envs}"
        )
        return

    # [2] Find pip index url.
    keys: list[str] = ["PIP_INDEX_URL", "PIP_EXTRA_INDEX_URL"]
    log(f"Searching for pip index url (envs: {keys})")
    if (env := find_env(envs=envs, keys=keys)) is None:
        log("Pip index url was not found")
        return
    log(f"Pip index url was found (source: {env[0]})")

    # [3] Parse pip index url.
    stripped_url: StrippedUrl = strip_url(url=env[1])

    def verbose_setenv(key: str, value: str) -> None:
        """Helper."""
        log(f"Setting environment variable: {key}")
        envs[key] = value

    # [4] Set PDM_PYPI_* envs.
    verbose_setenv("PDM_PYPI_URL", stripped_url.url)
    if stripped_url.auth is None:
        return
    verbose_setenv("PDM_PYPI_USERNAME", stripped_url.auth.username)
    verbose_setenv("PDM_PYPI_PASSWORD", stripped_url.auth.password)


def register_plugin(_: Core) -> None:
    """Entrypoint."""

    def run_plugin(project: Project, **_: Any) -> None:
        """Adapter."""
        process_pip_envs(
            envs=os.environ,
            log=functools.partial(project.core.ui.echo, verbosity=Verbosity.DETAIL),
        )

    pre_invoke.connect(run_plugin, weak=False)
