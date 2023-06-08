"""A pdm plugin that automatically converts PIP_*INDEX_URL to PDM_PYPI_* envs."""

from .plugin import register_plugin

__all__: tuple[str, ...] = ("register_plugin",)
