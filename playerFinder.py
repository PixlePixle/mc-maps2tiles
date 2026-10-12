import urllib.request
import parser
import os
import glob
import sys
import urllib.request
import json

def processPlayers(sourcePath, outputPath):
    filenames = []
    for filename in glob.glob(os.path.join(sourcePath, '*-*-*-*-*.dat')):
        filenames.append(filename)
    print(f"Files found: {len(filenames)}")

    UUIDDict = dict()
    if os.path.exists(os.path.join(outputPath, 'uuidDict.json')):
        with open(os.path.join(outputPath, 'uuidDict.json')) as file:
            UUIDDict = json.load(file)

    overworldPlayers = {}
    netherPlayers = {}
    endPlayers = {}
    allPlayers = {"overworld": overworldPlayers, "nether": netherPlayers, "end": endPlayers}

    print("====================================")
    for filename in filenames:
        temp = parser.parse(filename)
        [UUID, _unused] = os.path.basename(filename).split(".")
        # If the UUID is not found in our json, we'll query the minecraft api
        if UUID not in UUIDDict:
            print("UUID Not found")
            with urllib.request.urlopen("https://sessionserver.mojang.com/session/minecraft/profile/" + UUID) as data:
                UUIDDict[UUID] = json.loads(data.read().decode())["name"]

        # Prints the person it's currently on
        print(UUID)
        print(UUIDDict[UUID])
        print(f"Health: {temp['Health']}")
        print(f"X: {temp['Pos'][0]}")
        print(f"Y: {temp['Pos'][1]}")
        print(f"Z: {temp['Pos'][2]}")
        print("====================================")

# https://api.mcheads.org/head/${this.options.name}/32
        headImage = os.path.join(outputPath, 'icons', 'heads', UUIDDict[UUID] + '.png')
        if not os.path.exists(headImage):
            try:
                urllib.request.urlretrieve('https://api.mcheads.org/head/' + UUIDDict[UUID] + '/32', headImage)
            except Exception as e:
                print(f"Failed to fetch iamge: {e}")
        
        
        if temp["Dimension"] == "minecraft:overworld" or temp["dimension"] == 0:
            overworldPlayers[UUIDDict[UUID]] = {"Pos": temp["Pos"], "Health": temp["Health"]}
            if os.path.exists(os.path.join(sys.argv[2], "overworld")):
                with open(os.path.join(outputPath, "overworld", 'players.json'), "w") as file:
                    json.dump(overworldPlayers, file, sort_keys=True, indent=4)
        elif temp["Dimension"] == "minecraft:the_nether" or temp["dimension"] == -1:
            netherPlayers[UUIDDict[UUID]] = {"Pos": temp["Pos"], "Health": temp["Health"]}
            if os.path.exists(os.path.join(sys.argv[2], "nether")):
                with open(os.path.join(outputPath, "nether", 'players.json'), "w") as file:
                    json.dump(netherPlayers, file, sort_keys=True, indent=4)
        else: # "the_end"
            endPlayers[UUIDDict[UUID]] = {"Pos": temp["Pos"], "Health": temp["Health"]}
            if os.path.exists(os.path.join(sys.argv[2], "end")):
                with open(os.path.join(outputPath, "end", 'players.json'), "w") as file:
                    json.dump(endPlayers, file, sort_keys=True, indent=4)

    # Saves the UUIDS and username pairs together
    with open(os.path.join(outputPath, 'uuidDict.json'), "w") as file:
        json.dump(UUIDDict, file, sort_keys=True, indent=4)



###########################################

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

fileChange = False

class MyHandler(FileSystemEventHandler):

    def on_any_event(self, event):
        if event.is_directory:
            return None
        
        print(f'File {event.src_path} has been modified')
        global fileChange
        global timer
        if not fileChange:
            fileChange = True


def fileWatcher(sourcePath, outputPath):
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, sourcePath, recursive=False)
    global fileChange
    observer.start()
    print(f"Watching for changes in {sourcePath}")

    try:
        while True:
            time.sleep(1)
            if fileChange:
                processPlayers(sourcePath, outputPath)
                fileChange = False
    except KeyboardInterrupt:
        observer.stop()
    observer.join()




###########################################


if __name__ == "__main__":
    usage = '''
    Usage:
        py playerFinder.py <source dir> <output dir optional>
    '''
    if len( sys.argv ) < 3:
        print(usage)
        exit()
        
    sourcePath = os.path.join(sys.argv[1], 'players', 'data')
    # sourcePath = sys.argv[1]
    outputPath = sys.argv[2]
    processPlayers(sourcePath, outputPath)
    fileWatcher(sourcePath, outputPath)

    

# THIS IS FOR LATER FOR ACTUALLY SEEING WHO'S ONLINE
# import time
# def follow(serverLog):
#     serverLog.seek(0,2) # Go to the end of the file
#     while True:
#         line = serverLog.readline()
#         if not line:
#             time.sleep(0.1) # Sleep briefly
#             continue
#         yield line


