#!/bin/bash
node_dir=$( dirname "${BASH_SOURCE[0]}" )
source "$node_dir/.env"

"$node_dir/venv/Scripts/python.exe" -m flask --app "$node_dir/app.py" run --port $1
