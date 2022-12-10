#!/usr/bin/env bash

poetry run uvicorn --host 0.0.0.0 backend.main:app --reload