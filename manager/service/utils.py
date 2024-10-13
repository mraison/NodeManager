import random
import string
import pathlib
import subprocess
import os
import signal
from io import TextIOWrapper
from pathlib import Path

from NodeManager.node import NODE_DIR


def get_node_app_file_path():
    curr_path = pathlib.Path(__file__).parent.parent.parent.resolve()
    return str(curr_path / 'node/app.py')


def generate_unique_string(length=8):
    """Generates a unique random string of given length."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def _start_node():
    port = random.randint(5000, 5050)
    log = open(f'{port}.log', 'a')
    proc = subprocess.Popen(
        ['flask', '--app', str(NODE_DIR / 'app.py'), 'run', '--port', str(port)],
        stdout=log,
        stderr=log
    )

    return '127.0.0.1', port, str(proc.pid)


def _stop_node(pid: int):
    try:
        os.kill(pid, signal.SIGTERM)
    except OSError:
        pass

