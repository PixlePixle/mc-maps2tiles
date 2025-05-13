import time
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

usage = '''
Usage:
    py fileWatcher.py <source dir> <output dir>
'''

if len( sys.argv ) < 3:
    print(usage)
    exit()

sourcePath = sys.argv[1]
outputPath = sys.argv[2]
fileChange = False

fileChange = False
timer = 0

class MyHandler(FileSystemEventHandler):

    def on_any_event(self, event):
        if event.is_directory:
            return None
        
        print(f'File {event.src_path} has been modified')
        global fileChange
        global timer
        if not fileChange:
            fileChange = True
            timer = 30





if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, sourcePath, recursive=False)

    observer.start()
    print(f"Watching for changes in {sourcePath}")

    try:
        while True:
            time.sleep(1)
            if timer > 0:
                timer = timer -1
            if fileChange and timer == 0:
                print("Test")
                subprocess.run(["python3", "./mapCreator.py", sourcePath, outputPath])
                fileChange = False
    except KeyboardInterrupt:
        observer.stop()
    observer.join()