# pdm-pip-index-url

pdm-pip-index-url is pdm plugin that automatically converts `PIP_*INDEX_URL` to `PDM_PYPI_*` envs.

For each pdm sub-command invocation, pdm will search for `PIP_*INDEX_URL` environment variables to convert them to coressponding `PDM_PYPI_*` values (see `process_pip_envs` in [./plugin.py](./pdm_pip_index_url/plugin.py) for detailed logic description).

## Usage

1. Install plugin: `pdm self add pdm-pip-index-url`
