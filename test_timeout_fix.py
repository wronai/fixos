#!/usr/bin/env python3
"""Test the timeout suspension logic for user input."""

import signal
import time
from contextlib import contextmanager

# Simulate the timeout functions
_timeout_handler = None
_timeout_seconds = None
timeout_fired = False

def timeout_handler(signum, frame):
    global timeout_fired
    timeout_fired = True
    raise TimeoutError("Timeout fired!")

@contextmanager
def suspend_timeout():
    """Context manager to temporarily suspend session timeout during user input."""
    global _timeout_handler, _timeout_seconds
    try:
        signal.alarm(0)  # Cancel the active timeout
        yield
    finally:
        # Reinstate timeout if it was set
        if _timeout_handler and _timeout_seconds:
            signal.signal(signal.SIGALRM, _timeout_handler)
            signal.alarm(_timeout_seconds)

def setup_timeout_ref(seconds, handler):
    """Store timeout handler and seconds for later reinstatement."""
    global _timeout_handler, _timeout_seconds
    _timeout_handler = handler
    _timeout_seconds = seconds

# Test
print("Starting timeout suspension test...")
setup_timeout_ref(2, timeout_handler)
signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(2)

try:
    print("Timeout is active (2 seconds)...")
    time.sleep(0.5)
    
    with suspend_timeout():
        print("Inside suspend_timeout context - timeout should be suspended")
        time.sleep(3)  # This should NOT trigger timeout
        print("✅ Successfully waited 3 seconds inside suspend_timeout")
    
    # After exiting context, timeout should be re-established
    print("Timeout should be re-established now")
    timeout_fired = False
    time.sleep(3)  # This SHOULD trigger timeout
    
except TimeoutError as e:
    if timeout_fired:
        print("✅ Timeout correctly re-established after suspend context")
    else:
        print("❌ Timeout fired at wrong time")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
finally:
    signal.alarm(0)

print("Test complete!")
