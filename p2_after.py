"""
PROBLEM 2 — Print "HELLO" (AFTER: With Semaphores)
===================================================
3 processes coordinated by semaphores to print
exactly "HELLO" once, then all stop.

Semaphores:
  a = 1  — Process 1 is allowed to start immediately
  b = 0  — Process 2 is blocked; waits for Process 1 to finish HE
  c = 0  — Process 3 is blocked; waits for Process 2 to finish LL

Execution order enforced:
  P1: wait(a) → print H → print E → signal(b)
  P2: wait(b) → print L → signal(b)   [releases itself for 2nd L]
      wait(b) → print L → signal(c)
  P3: wait(c) → print O → done
"""

import threading
import time

result = []

# ✅ Semaphores
a = threading.Semaphore(1)   # P1 can start right away
b = threading.Semaphore(0)   # P2 waits for P1
c = threading.Semaphore(0)   # P3 waits for P2


def process1():
    a.acquire()                        # wait(a) — allowed since a=1
    print("  Process 1: wait(a) passed  → printing 'H'")
    result.append('H')
    time.sleep(0.05)

    print("  Process 1:                 → printing 'E'")
    result.append('E')
    time.sleep(0.05)

    b.release()                        # signal(b) — unblock Process 2
    print("  Process 1: signal(b)       → Process 1 done\n")
    # a is now 0; if loop tried wait(a) again it would block → process halts


def process2():
    # --- First L ---
    b.acquire()                        # wait(b) — blocks until P1 signals
    print("  Process 2: wait(b) passed  → printing first 'L'")
    result.append('L')
    time.sleep(0.05)

    b.release()                        # signal(b) — release for own second iteration
    print("  Process 2: signal(b)")

    # --- Second L ---
    b.acquire()                        # wait(b) again
    print("  Process 2: wait(b) passed  → printing second 'L'")
    result.append('L')
    time.sleep(0.05)

    c.release()                        # signal(c) — unblock Process 3
    print("  Process 2: signal(c)       → Process 2 done\n")


def process3():
    c.acquire()                        # wait(c) — blocks until P2 signals
    print("  Process 3: wait(c) passed  → printing 'O'")
    result.append('O')
    print("  Process 3: done\n")


if __name__ == "__main__":
    print()
    print("╔══════════════════════════════════════════════════════════╗")
    print("║   PROBLEM 2 — AFTER (With Semaphores)                   ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()
    print("  Semaphores:  a=1, b=0, c=0")
    print()
    print("  --- Execution Trace ---")
    print()

    t1 = threading.Thread(target=process1)
    t2 = threading.Thread(target=process2)
    t3 = threading.Thread(target=process3)

    # All start at the same time — semaphores handle the order
    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()

    output_str = "".join(result)
    print(f"  Final output : \"{output_str}\"")
    print(f"  Expected     : \"HELLO\"")
    print()

    if output_str == "HELLO":
        print("  ✅ Correct! Semaphores enforced:")
        print("     • H and E printed first (Process 1 had a=1 to start)")
        print("     • L printed twice in order (Process 2 signaled itself)")
        print("     • O printed last (Process 3 waited for both L's)")
        print("     • Exactly 'HELLO' once — all processes halted after")
    else:
        print(f"  ❌ Wrong output: '{output_str}'")
    print()
