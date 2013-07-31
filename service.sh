#!/bin/bash

source .env/bin/activate
python scripts/daemon.py "$@"
deactivate
