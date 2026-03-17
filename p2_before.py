"""
PROBLEM 2 — Print "HELLO" (BEFORE: No Semaphores)
==================================================
3 processes run concurrently with no coordination.

  Process 1: prints H then E  (loops)
  Process 2: prints L         (loops)
  Process 3: prints O         (loops)

Without semaphores they all run at the same time
and produce random garbage instead of "HELLO".
"""

import threading
import time
import random

result = []
output_lock = threading.Lock()
stop_event = threading.Event()


def process1():
    while not stop_event.is_set():
        with output_lock:
            result.append('H')
            result.append('E')
        time.sleep(random.uniform(0, 0.02))


def process2():
    while not stop_event.is_set():
        with output_lock:
            result.append('L')
        time.sleep(random.uniform(0, 0.015))


def process3():
    while not stop_event.is_set():
        with output_lock:
            result.append('O')
        time.sleep(random.uniform(0, 0.018))


if __name__ == "__main__":
    print()
    print("╔══════════════════════════════════════════════════════════╗")
    print("║   PROBLEM 2 — BEFORE (No Semaphores)                    ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()
    print("  All 3 processes run freely with no coordination.")
    print()

    t1 = threading.Thread(target=process1)
    t2 = threading.Thread(target=process2)
    t3 = threading.Thread(target=process3)

    t1.start()
    t2.start()
    t3.start()

    time.sleep(0.08)
    stop_event.set()

    t1.join()
    t2.join()
    t3.join()

    output_str = "".join(result[:15])
    print(f"  Output produced : \"{output_str}\"")
    print(f"  Expected        : \"HELLO\"")
    print()

    violations = []
    if not "".join(result).startswith("HELLO") or len(result) != 5:
        violations.append(f"Output is NOT exactly 'HELLO'")
    if result.count('H') > 1 or result.count('E') > 1:
        violations.append("H or E printed more than once")
    if len(result) > 5:
        violations.append(f"Printed {len(result)} characters instead of 5")

    if violations:
        print("  ❌ Violations:")
        for v in violations:
            print(f"     • {v}")
    else:
        print("  (Happened to look OK — non-deterministic, run again!)")
    print()
