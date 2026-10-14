#!/usr/bin/env python3
"""Orchestrate a real two-JVM Putt Putt Paradise online capture (Opus final round r5, 2026-10-06).

Purpose: record what the host and the guest each see and hear during genuine direct-TCP play.
Inputs: --rom, --jar, --classes (compiled GolfPromoCapture), --classpath (engine classpath), --out.
Both JVMs run GolfPromoCapture (online-host / online-guest). This script only sends logical
Genesis buttons, one row at a time to each peer in turn, and reads their STATE lines; it never
touches gameplay. Rows are lockstepped by command, while the room itself stays asynchronous TCP.
"""
import argparse
import json
import subprocess
import sys
import time
from pathlib import Path


class Peer:
    def __init__(self, role, args, out):
        out.mkdir(parents=True, exist_ok=False)
        self.role = role
        self.log = open(out / "capture.log", "w")
        self.proc = subprocess.Popen(
            ["java", "-cp", f"{args.classes}:{args.classpath}", "com.openggf.mods.code.GolfPromoCapture",
             str(args.rom), str(args.jar), str(out), "online-" + role],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=self.log, text=True, cwd=args.repo)
        self.state = {}

    def send(self, command):
        self.proc.stdin.write(command + "\n"); self.proc.stdin.flush()
        while True:
            line = self.proc.stdout.readline()
            if not line:
                raise RuntimeError(f"{self.role} exited during {command}")
            if line.startswith("STATE|"):
                self.state = dict(item.split("=", 1) for item in line.strip().split("|")[1:])
                return self.state
            self.log.write(line)

    def quit(self):
        try:
            self.proc.stdin.write("QUIT\n"); self.proc.stdin.flush()
            self.proc.wait(timeout=120)
        finally:
            self.log.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("rom", "jar", "classes", "classpath", "out", "repo"):
        parser.add_argument("--" + name, required=True)
    args = parser.parse_args()
    out = Path(args.out)
    host = Peer("host", args, out / "online-host")
    time.sleep(6)  # Let the host bind its listener before the guest's title selects Join.
    guest = Peer("guest", args, out / "online-guest")
    rows = 0
    timeline = []

    def row(host_buttons="-", guest_buttons="-"):
        nonlocal rows
        host.send(f"STEP 1 {host_buttons}"); guest.send(f"STEP 1 {guest_buttons}")
        rows += 1
        time.sleep(0.004)  # Give the socket workers a moment; the rows themselves stay paired.

    def pump(condition, limit, what):
        for _ in range(limit):
            if condition():
                return
            row()
        if not condition():
            raise RuntimeError(f"{what}: host={host.state} guest={guest.state}")

    def mark(name):
        host.send(f"EVENT {name}"); guest.send(f"EVENT {name}")
        timeline.append({"row": rows, "event": name, "host": dict(host.state), "guest": dict(guest.state)})
        print(name, "host", host.state, "guest", guest.state, flush=True)

    def ready(owner):
        both_handoff = lambda: host.state.get("phase") == "HANDOFF" and guest.state.get("phase") == "HANDOFF"
        pump(both_handoff, 600, "handoff on both peers")
        mark(f"handoff-{owner}")
        for _ in range(80):
            row()  # Both peers show the card: owner prompt and spectator wait.
        if owner == 0: row("A", "-")
        else: row("-", "A")
        pump(lambda: host.state.get("phase") == "AIM" and guest.state.get("phase") == "AIM", 200, "ready transition")
        mark(f"ready-{owner}")
        for _ in range(40):
            row()

    def shot(owner, direction, loft, power):
        def press(buttons, count=1):
            for _ in range(count):
                row(buttons, "-") if owner == 0 else row("-", buttons)
        mark(f"aim-{owner}-{direction}-{loft}-{power}")
        press("-"); press("L" if direction < 0 else "R")
        if loft: press("U", loft)
        press("-"); press("A")
        local = host if owner == 0 else guest
        if local.state.get("stage") == "SPIN":
            press("-", 60); press("A")
        press("-", power); press("A")
        mark(f"shot-{owner}")

    def settle(next_owner, what):
        pump(lambda: host.state.get("owner") == str(next_owner) and host.state.get("phase") in ("HANDOFF", "AIM")
             and guest.state.get("turn") == host.state.get("turn"), 3000, what)
        mark(f"turn-to-{next_owner}")

    pump(lambda: host.state.get("ready") == "true" and guest.state.get("ready") == "true", 2400, "room handshake")
    mark("room-ready")
    route = [(1, 0, 30), (1, 40, 60), (1, 0, 45)]
    for index, (direction, loft, power) in enumerate(route):
        ready(0); shot(0, direction, loft, power); settle(1, f"host shot {index + 1}")
        ready(1)
        if index == 1:
            # The guest rewinds its moving chip from the Start menu; the host restores and refunds it.
            shot(1, direction, loft, power)
            for _ in range(70): row()
            mark("guest-rewind-request")
            for buttons in ("S", "-", "D", "-", "A"): row("-", buttons)
            pump(lambda: host.state.get("phase") == "AIM" and guest.state.get("phase") == "AIM"
                 and host.state.get("owner") == "1", 400, "guest rewind restored")
            mark("guest-rewind-restored")
            for _ in range(30): row()
        shot(1, direction, loft, power); settle(0, f"guest shot {index + 1}")
    for _ in range(120): row()
    mark("capture-end")
    host.quit(); guest.quit()
    (out / "online-timeline.json").write_text(json.dumps({"rows": rows, "events": timeline}, indent=1) + "\n")
    print("rows", rows)


if __name__ == "__main__":
    sys.exit(main())
