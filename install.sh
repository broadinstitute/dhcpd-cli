#!/bin/bash

SCRIPT_DIR="$( cd -P "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

python -m virtualenv --clear "${SCRIPT_DIR}/.venv"

# shellcheck source=/dev/null
source "${SCRIPT_DIR}/.venv/bin/activate"

pip install -r requirements.txt

deactivate
