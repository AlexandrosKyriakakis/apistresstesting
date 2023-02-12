#!/bin/bash

set -o xtrace
mypy --ignore-missing-imports --config-file pyproject.toml src/*.py
pre-commit clean && pre-commit install
git ls-files -- '*.py' | xargs pre-commit run --files
exit_code="$?"
if [ $exit_code -ne 0 ]
then
exit $exit_code
fi
pylint --rcfile=pylintrc --fail-under=7 src
