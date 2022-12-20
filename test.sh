#!/usr/bin/env bash

rm -rf ./sql_app_test.db
POETRY_DOTENV_LOCATION=./.env.testing poetry run python -m pytest -v