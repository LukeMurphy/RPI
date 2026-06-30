"""
Launch several pieces in parallel, each in its own Process.
A per-piece Queue accepts commands; a shared reply Queue returns status.

Commands (put on cmd_q):
  "stop"   — terminate the piece
  "ping"   — reply with current pid / poll status
  None     — sentinel, same effect as "stop"

Usage (run from RPI/test-code/):
  python3 multi-proc-tester-4.py
"""

import sys
import subprocess
import time
from multiprocessing import Process, Queue

PLAYER = "/Users/lamshell/Documents/Dev/LEDELI/RPI/player.py"

PIECES = [
    "dev/_in_progress_revisit/concentric-particles-v4.cfg",
    "dev/_in_progress_revisit/concentric-particles-v4.cfg"]


# ---------------------------------------------------------------------------

def run_piece(cfg: str, cmd_q: Queue, reply_q: Queue) -> None:
    """Process target: launch player.py and relay Queue-based commands."""
    proc = subprocess.Popen(
        ["python3", PLAYER, "-cfg", cfg],
        cwd="..",
    )
    reply_q.put({"cfg": cfg, "pid": proc.pid, "status": "started"})

    while True:
        # Non-blocking command check
        try:
            cmd = cmd_q.get(timeout=0.25)
        except Exception:
            cmd = None

        if cmd in ("stop", None):
            proc.terminate()
            reply_q.put({"cfg": cfg, "status": "stopped"})
            return

        if cmd == "ping":
            reply_q.put({"cfg": cfg, "pid": proc.pid, "poll": proc.poll()})

        # Piece exited on its own
        if proc.poll() is not None:
            reply_q.put({"cfg": cfg, "status": "exited", "code": proc.poll()})
            return


# ---------------------------------------------------------------------------

def launch_pieces(pieces: list[str], run_seconds: float = 10.0):
    """Spawn one Process per piece, run for run_seconds, then stop all."""
    reply_q: Queue = Queue()
    entries = []

    for cfg in pieces:
        cmd_q: Queue = Queue()
        p = Process(target=run_piece, args=(cfg, cmd_q, reply_q), name=cfg)
        p.start()
        entries.append((cfg, cmd_q, p))

    # Collect startup confirmations
    for _ in pieces:
        print("[main]", reply_q.get())

    # Run until timeout (or add your own logic / input loop here)
    time.sleep(run_seconds)

    # Send stop to every piece
    for _cfg, cq, _p in entries:
        cq.put("stop")

    for _cfg, _cq, p in entries:
        p.join(timeout=5)
        if p.is_alive():
            p.kill()

    # Drain remaining replies
    while not reply_q.empty():
        print("[main]", reply_q.get())

    print("[main] all done.")


# ---------------------------------------------------------------------------

if __name__ == "__main__":
    launch_pieces(PIECES, run_seconds=30.0)
