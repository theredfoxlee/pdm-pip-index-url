# pdm-pip-index-url

[![GitHub Workflow - Status](https://img.shields.io/github/actions/workflow/status/theredfoxlee/pdm-pip-index-url/ci.yaml?label=tests)](https://github.com/theredfoxlee/pdm-pip-index-url/actions/workflows/ci.yaml)
![PyPI - Version](https://img.shields.io/pypi/v/pdm-pip-index-url?color=%2334D058)
[![PyPI - Python Versions](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-blue)](./pyproject.toml)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/pdm-pip-index-url)](https://pypistats.org/packages/pdm-pip-index-url)
![PyPI - Format](https://img.shields.io/pypi/format/pdm-pip-index-url)

`pdm-pip-index-url` is a pdm plugin that automatically converts `PIP_*INDEX_URL` to `PDM_PYPI_*` envs.

For each pdm sub-command invocation, pdm will search for `PIP_*INDEX_URL` environment variables to convert them to coressponding `PDM_PYPI_*` values (see `process_pip_envs` in [./plugin.py](./pdm_pip_index_url/plugin.py) for detailed logic description).

## Usage

1. Install plugin: `pdm self add pdm-pip-index-url`

### Logging

Turn on logging by adding `-v` to executed command, e.g.: `pdm add -v black`.
