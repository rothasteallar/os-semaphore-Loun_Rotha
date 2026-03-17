"""
PROBLEM 1 — Particle Buffer (BEFORE: No Semaphores)
====================================================
3 producers place particle pairs into a shared buffer.
1 consumer takes pairs out to package them.

No synchronization — race conditions happen freely.
"""

import threading
import time
import random
from collections import deque

BUFFER_MAX = 100

buffer = deque()
violations = []
log = []
pair_counter = [0]
stop_event = threading.Event()


def producer(pid):
    for _ in range(6):
        if stop_event.is_set():
            break

        pair_id = f"P{pid}-{pair_counter[0]}"
        pair_counter[0] += 1

        p1 = f"{pair_id}-A"
        p2 = f"{pair_id}-B"

        # ❌ No check for free space
        # ❌ No lock — another producer can slip between placing P1 and P2

        if len(buffer) < BUFFER_MAX:
            buffer.append(p1)
            log.append(f"  Producer-{pid} placed {p1:<14}  [buffer size={len(buffer)}]")

        time.sleep(random.uniform(0, 0.02))   # <-- context switch opportunity

        if len(buffer) < BUFFER_MAX:
            buffer.append(p2)
            log.append(f"  Producer-{pid} placed {p2:<14}  [buffer size={len(buffer)}]")
        else:
            msg = f"  ❌ VIOLATION: Producer-{pid} dropped {p2} — buffer full! Pair BROKEN."
            violations.append(msg)
            log.append(msg)


def consumer():
    fetched = 0
    while fetched < 10:
        # ❌ No wait — may see only 1 particle
        if len(buffer) == 1:
            msg = "  ❌ VIOLATION: Consumer sees only 1 particle — half-pair fetch!"
            violations.append(msg)
            log.append(msg)

        if len(buffer) >= 2:
            p1 = buffer.popleft()
            p2 = buffer.popleft()

            base1 = p1.rsplit("-", 1)[0]
            base2 = p2.rsplit("-", 1)[0]

            if base1 != base2:
                msg = f"  ❌ VIOLATION: Mismatched pair!  Got {p1} + {p2}  (NOT a real pair)"
                violations.append(msg)
                log.append(msg)
            else:
                log.append(f"  Consumer packaged: {p1} + {p2}  ✓")

            fetched += 1
        else:
            time.sleep(0.005)


if __name__ == "__main__":
    print()
    print("╔══════════════════════════════════════════════════════════╗")
    print("║   PROBLEM 1 — BEFORE (No Semaphores)                    ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()

    threads = [threading.Thread(target=producer, args=(i,)) for i in range(3)]
    c = threading.Thread(target=consumer)

    for t in threads:
        t.start()
    c.start()

    time.sleep(0.4)
    stop_event.set()

    for t in threads:
        t.join(timeout=1)
    c.join(timeout=1)

    print("  --- Event Log ---")
    for line in log[:30]:
        print(line)

    print()
    if violations:
        print(f"  ⚠  {len(violations)} violation(s) detected:")
        for v in violations:
            print(f"    {v}")
    else:
        print("  No violations this run (race conditions are non-deterministic — try again!)")
    print()
