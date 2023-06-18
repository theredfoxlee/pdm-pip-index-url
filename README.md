# pdm-pip-index-url

![GitHub Workflow - Status](https://img.shields.io/github/actions/workflow/status/theredfoxlee/pdm-pip-index-url/ci.yaml?label=tests)
[![PyPI - Python Versions](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-blue)](./pyproject.toml)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/pdm-pip-index-url)](https://pypistats.org/packages/pdm-pip-index-url)
![PyPI - Format](https://img.shields.io/pypi/format/pdm-pip-index-url)

`pdm-pip-index-url` is a pdm plugin that automatically converts `PIP_*INDEX_URL` to `PDM_PYPI_*` envs.

For each pdm sub-command invocation, pdm will search for `PIP_*INDEX_URL` environment variables to convert them to coressponding `PDM_PYPI_*` values (see `process_pip_envs` in [./plugin.py](./pdm_pip_index_url/plugin.py) for detailed logic description).

## Usage

1. Install plugin: `pdm self add pdm-pip-index-url`

### Logging

Turn on logging by adding `-v` to executed command, e.g.: `pdm add -v black`.

### Example [Use Case]

Consider a scenario where you are using PDM in an environment that does not provide a way to authenticate it to a private PyPI server but supports pip authentication (e.g., Azure Pipelines). Here is an example:

```yaml
# 1. Set PIP_INDEX_URL for <private-feed>.
- task: PipAuthenticate@1
  inputs:
    artifactFeeds: <private-feed>
# 2. Install this plugin.
- script: pdm self add pdm-pip-index-url
# 3. Use PIP_INDEX_URL env to install <private-package> from <private-feed>.
- script: pdm add <private-package>
```