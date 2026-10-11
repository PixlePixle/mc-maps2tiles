import urllib.request
import parser
import os
import glob
import sys
import urllib.request
import json
from pprint import pprint

usage = '''
Usage:
    py playerFinder.py <source dir> <output dir optional>
'''

if len( sys.argv ) < 3:
    print(usage)
    exit()

sourcePath = sys.argv[1]
outputPath = sys.argv[2]

filenames = []
for filename in glob.glob(os.path.join(sourcePath, '*-*-*-*-*.dat')):
    filenames.append(filename)
print(f"Files found: {len(filenames)}")

UUIDDict = dict()
if os.path.exists(os.path.join(outputPath, 'uuidDict.txt')):
    with open(os.path.join(outputPath, 'uuidDict.txt')) as file:
        UUIDDict = json.load(file)
for filename in filenames:
    temp = parser.parse(filename)
    [UUID, _unused] = os.path.basename(filename).split(".")
    print(UUID)
    if UUID not in UUIDDict:
        print("UUID NOT FOUND")
        with urllib.request.urlopen("https://sessionserver.mojang.com/session/minecraft/profile/" + UUID) as data:
            UUIDDict[UUID] = json.loads(data.read().decode())["name"]
    else:
        print(f"UUID FOUND: {UUID}")
    print(UUIDDict[UUID])
    print(json.dumps(UUIDDict, sort_keys=True, indent=4))
    print(f"X: {temp['Pos'][0]}")
    print(f"Y: {temp['Pos'][1]}")
    print(f"Z: {temp['Pos'][2]}")
    
with open(os.path.join(outputPath, 'uuidDict.txt'), "w") as file:
    json.dump(UUIDDict, file, sort_keys=True, indent=4)
    
    # print(f"{data}")
# print(f"Player maps count: {len(overworldMapData) + len(netherMapData) + len(endMapData)}")



# import time
# def follow(serverLog):
#     serverLog.seek(0,2) # Go to the end of the file
#     while True:
#         line = serverLog.readline()
#         if not line:
#             time.sleep(0.1) # Sleep briefly
#             continue
#         yield line


