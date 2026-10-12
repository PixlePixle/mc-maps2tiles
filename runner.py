import sys
import signal
import threading
from subprocess import Popen, TimeoutExpired

usage = """
Usage:
    python runner.py <source dir> <output dir>
"""

if len(sys.argv) < 3:
    print(usage)
    sys.exit(1)

sourcePath = sys.argv[1]
outputPath = sys.argv[2]

processes = []
shutdown_event = threading.Event()

def shutdown(signum=None, frame=None):
    if shutdown_event.is_set():
        return

    shutdown_event.set()

    for process in processes:
        if process.poll() is None:
            process.terminate()

    for process in processes:
        try:
            process.wait(timeout=5)
        except TimeoutExpired:
            process.kill()
            process.wait()

    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    try:
        processes.append(
            Popen(["python3", "./mapCreator.py", sourcePath, outputPath])
        )
        processes.append(
            Popen(["python3", "./playerFinder.py", sourcePath, outputPath])
        )

        print("Press Ctrl+C to stop.")

        shutdown_event.wait()

    finally:
        shutdown()