import random
import string
import time
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


class StopNodeException(Exception):
    pass

def _stop_node(pid: int, port: int = 0, timeout: float = 5.0, remove_log: bool = True):
    try:
        os.kill(pid, signal.SIGTERM)
    except OSError:
        pass

    timeout_time = time.time() + timeout
    while True:
        if time.time() >= timeout_time:
            raise StopNodeException("pid removal timeout.")
            return
        try:
            os.kill(pid, 0)
            time.sleep(0.1)
        except OSError:
            break
        except Exception:
            pass
        finally:
            time.sleep(0.1)

    if remove_log:
        log_f = pathlib.Path(f'{port}.log')
        log_f.unlink()
