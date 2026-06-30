"""
Launch two player.py instances via multiprocessing.Manager.

Player processes are launched directly with Popen from the main process —
no intermediate Process layer. Daemon threads monitor each player and
write status back into the Manager's shared dict.

Usage (from repo root):
    python test-code/player-duo-manager.py
    python test-code/player-duo-manager.py --cfg staging/p4-512px-in-parts/celestials-m-1.cfg
"""

import argparse
import os
import subprocess
import sys
import threading
import time
from multiprocessing import Manager

BASE_DIR = "/Users/lamshell/Documents/Dev/LEDELI/RPI"
DEFAULT_CFG = "staging/p4-512px-in-parts/celestials-m-1.cfg"
PLAYER = os.path.join(BASE_DIR, "player.py")


def _watch(proc: subprocess.Popen, player_id: str, state: dict) -> None:
    """Daemon thread — blocks on proc.wait() then records the exit status."""
    proc.wait()
    state[player_id] = f"exited (returncode={proc.returncode})"


def launch_player(player_id: str, cfg: str, state: dict) -> subprocess.Popen:
    cmd = [sys.executable, PLAYER, "-cfg", cfg]
    proc = subprocess.Popen(cmd, cwd=BASE_DIR)
    state[player_id] = f"running (pid={proc.pid})"
    t = threading.Thread(target=_watch, args=(proc, player_id, state), daemon=True)
    t.start()
    return proc


def main() -> None:
    parser = argparse.ArgumentParser(description="Launch two player.py instances")
    parser.add_argument("--cfg", default=DEFAULT_CFG)
    parser.add_argument("--status-interval", type=float, default=1.0)
    args = parser.parse_args()

    with Manager() as manager:
        state = manager.dict()

        procs = [
            launch_player(f"player_{i}", args.cfg, state)
            for i in range(2)
        ]


        while any(p.poll() is None for p in procs):
            print("[manager] status:", dict(state))
            time.sleep(args.status_interval)


        # for p in procs:
        #     p.wait()

        print("[manager] final state:", dict(state))

if __name__ == '__main__':
    main()