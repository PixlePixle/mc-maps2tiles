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
    py playerFinder.py <source dir> <whitelist.json> <output file>
'''

if len( sys.argv ) < 4:
    print(usage)
    exit()

sourcePath = sys.argv[1]
whitelistFile = sys.argv[2]
outputPath = sys.argv[3]

whitelistFile = open(os.path.join(whitelistFile))
print(whitelistFile.read())

filenames = []
for filename in glob.glob(os.path.join(sourcePath, '*-*-*-*-*.dat')):
    filenames.append(filename)
print(f"Files found: {len(filenames)}")

for filename in filenames:
    temp = parser.parse(filename)
    print(f"X: {temp['Pos'][0]}")
    print(f"Y: {temp['Pos'][1]}")
    print(f"Z: {temp['Pos'][2]}")

    
    # print(f"{data}")
# print(f"Player maps count: {len(overworldMapData) + len(netherMapData) + len(endMapData)}")