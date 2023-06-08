"""A pdm plugin that automatically converts PIP_*INDEX_URL to PDM_PYPI_* envs."""

from typing import Tuple

from .plugin import register_plugin

__all__: Tuple[str, ...] = ("register_plugin",)
