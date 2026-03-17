"""
PROBLEM 1 — Particle Buffer (AFTER: With Semaphores)
=====================================================
3 producers place particle pairs into a shared buffer.
1 consumer takes pairs out to package them.

Semaphores used:
  spaces = Semaphore(50)  — tracks free pair-slots (50 pairs max)
  pairs  = Semaphore(0)   — tracks complete pairs ready to consume
  mutex  = Semaphore(1)   — ensures P1+P2 are placed atomically
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
counter_lock = threading.Lock()
stop_event = threading.Event()

# ✅ Semaphores
spaces = threading.Semaphore(50)   # 50 pair-slots available in buffer
pairs  = threading.Semaphore(0)    # 0 complete pairs ready yet
mutex  = threading.Semaphore(1)    # 1 = unlocked, ensures atomic pair placement


def producer(pid):
    for _ in range(4):
        if stop_event.is_set():
            break

        with counter_lock:
            pair_id = f"P{pid}-{pair_counter[0]}"
            pair_counter[0] += 1

        p1 = f"{pair_id}-A"
        p2 = f"{pair_id}-B"

        # ✅ Rule 1 & 3: wait until there is a free pair-slot
        spaces.acquire()

        # ✅ Rule 2: lock the buffer so P1 and P2 are placed with nothing in between
        mutex.acquire()
        buffer.append(p1)
        buffer.append(p2)
        log.append(f"  Producer-{pid} placed [{p1}, {p2}]  [buffer size={len(buffer)}]")
        mutex.release()

        # ✅ Tell consumer one more pair is ready
        pairs.release()

        time.sleep(random.uniform(0.01, 0.04))


def consumer():
    packaged = 0
    while packaged < 6:
        # ✅ Rule 4: block until a complete pair is available
        pairs.acquire()

        mutex.acquire()
        p1 = buffer.popleft()
        p2 = buffer.popleft()
        mutex.release()

        # Return the slot to the pool
        spaces.release()

        base1 = p1.rsplit("-", 1)[0]
        base2 = p2.rsplit("-", 1)[0]

        if base1 != base2:
            violations.append(f"  ❌ Mismatched pair: {p1} + {p2}")
        else:
            log.append(f"  Consumer packaged: {p1} + {p2}  ✓  [buffer size={len(buffer)}]")

        packaged += 1


if __name__ == "__main__":
    print()
    print("╔══════════════════════════════════════════════════════════╗")
    print("║   PROBLEM 1 — AFTER (With Semaphores)                   ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()
    print("  Semaphores:")
    print("    spaces = Semaphore(50)  ← 50 free pair-slots")
    print("    pairs  = Semaphore(0)   ← 0 pairs ready to consume")
    print("    mutex  = Semaphore(1)   ← unlocked, for atomic placement")
    print()

    threads = [threading.Thread(target=producer, args=(i,)) for i in range(3)]
    c = threading.Thread(target=consumer)

    for t in threads:
        t.start()
    c.start()

    time.sleep(0.5)
    stop_event.set()

    for t in threads:
        t.join(timeout=2)
    c.join(timeout=2)

    print("  --- Event Log ---")
    for line in log:
        print(line)

    print()
    if violations:
        print(f"  ❌ Violations: {violations}")
    else:
        print("  ✅ Zero violations — all rules enforced:")
        print("     • Pairs always placed atomically (mutex)")
        print("     • Consumer never fetched from empty buffer (pairs semaphore)")
        print("     • Buffer capacity never exceeded (spaces semaphore)")
    print()
