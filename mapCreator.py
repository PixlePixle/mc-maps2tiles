import parser
import math
import os
import glob
from PIL import Image
from tqdm import tqdm
from collections import defaultdict
import sys

# The base map colors used by Minecraft. Each one is multiplied to get all the possible map colors
baseColors = [(0, 0, 0, 0),
              (127, 178, 56),
              (247, 233, 163),
              (199, 199, 199),
              (255, 0, 0),
              (160, 160, 255),
              (167, 167, 167),
              (0, 124, 0),
              (255, 255, 255),
              (164, 168, 184),
              (151, 109, 77),
              (112, 112, 112),
              (64, 64, 255),
              (143, 119, 72),
              (255, 252, 245),
              (216, 127, 51),
              (178, 76, 216),
              (102, 153, 216),
              (229, 229, 51),
              (127, 204, 25),
              (242, 127, 165), 
              (76, 76, 76),
              (153, 153, 153),
              (76, 127, 153),
              (127, 63, 178),
              (51, 76, 178),
              (102, 76, 51),
              (102, 127, 51),
              (153, 51, 51),
              (25, 25, 25),
              (250, 238, 77),
              (92, 219, 213),
              (74, 128, 255),
              (0, 217, 58),
              (129, 86, 49),
              (112, 2, 0),
              (209, 177, 161),
              (159, 82, 36),
              (149, 87, 108),
              (112, 108, 138),
              (186, 133, 36),
              (103, 117, 53),
              (160, 77, 78),
              (57, 41, 35),
              (135, 107, 98),
              (87, 92, 92),
              (122, 73, 88),
              (76, 62, 92),
              (76, 50, 35),
              (76, 82, 42),
              (142, 60, 46),
              (37, 22, 16),
              (189, 48, 49),
              (148, 63, 97),
              (92, 25, 29),
              (22, 126, 134),
              (58, 142, 140),
              (86, 44, 62),
              (20, 180, 133),
              (100, 100, 100),
              (216, 175, 147),
              (127, 167, 150)]

# The multipliers used by Minecraft
mapColorMultipliers = [180, 220, 255, 135]

def colorMultipler(baseColorTuple, multiplier):
    # https://minecraft.wiki/w/Map_item_format#Map_colors
    return tuple( math.floor((a * multiplier)/255) for a in baseColorTuple)

# Each color in data colors should correspond to the index in here.
allColors = [colorMultipler(a, b) for a in baseColors for b in mapColorMultipliers]

# Big section = 0 -> 2048
# Anything 0 < x < 2048 is part of big section 0
#
scaleDict = {0: 128,
             1: 256,
             2: 512,
             3: 1024,
             4: 2048}

scaleToZoom = {0: 4,
               1: 3,
               2: 2,
               3: 1,
               4: 0}

# Returns the top left of the chunk the item belongs to.
# For example, we have a map with topleft of 64, 64 and we want to find the top left for corresponding scale 4 map
# roundDown([64, 64], 4) = [0, 0]
# Useful for if we use a dict where the keys are the top left of x scale and the values are the list of items in that chunk
def roundDown(anchor, scale):
    return tuple( value - (value % scaleDict[scale]) for value in anchor )

# Returns the bottom right coords depending on scale. Useful for knowing where to crop
def bottomRight(topLeft, scale):
    return [value + scaleDict[scale] for value in topLeft]

# Gets the anchor on the 0-2048 scale
def normalizeAnchor(anchor):
    return tuple( abs(value % 2048) for value in anchor )

# Returns the starting index for folder/file
def folderFileNames(level4Coords, scale):
    return tuple( value // scaleDict[scale] for value in level4Coords)

# Everything above is base setup for processing
# -----------------------------------------------
# Everything below is for image processing based on above data

usage = '''
Usage:
    py mapCreator.py <source dir> <output dir>
'''

if len( sys.argv ) < 3:
    print(usage)
    exit()

sourcePath = sys.argv[1]
outputPath = sys.argv[2]

# Gets all files in the source directory
filenames = []
for filename in glob.glob(os.path.join(sourcePath, 'map_*.dat')):
    filenames.append(filename)
print(f"Files found: {len(filenames)}")

# Iterates over the source directory files and selects what should be player maps only.
overworldMapData = {}
netherMapData = {}
endMapData = {}
for filename in tqdm(filenames, desc=('Picking player maps')):
    temp = parser.parse(filename)
    temp = temp["data"]
    if "scale" not in temp:
        temp["scale"] = 0
    if "unlimitedTracking" not in temp:
        temp["unlimitedTracking"] = 0
    if temp["unlimitedTracking"] == 0:
        temp["colors"] = [allColors[a] for a in temp["colors"]]
        temp["epoch"] = os.path.getmtime(filename)
        # Set's the anchor. This is the center of the top left most scale 0 map as this lets us start at 0,0
        temp["anchor"] = [temp["xCenter"] - (64 * 2 ** temp["scale"]) + 64, temp["zCenter"] - (64 * 2 ** temp["scale"]) + 64]
        if temp["dimension"] == "minecraft:overworld":
            overworldMapData[filename] = temp
        elif temp["dimension"] == "minecraft:the_nether":
            netherMapData[filename] = temp
        else:
            endMapData[filename] = temp
print(f"Player maps count: {len(overworldMapData) + len(netherMapData) + len(endMapData)}")

# sort mapData by time modified
overworldMapData = dict(sorted(overworldMapData.items(), key=lambda item: item[1]["epoch"]))
netherMapData = dict(sorted(netherMapData.items(), key=lambda item: item[1]["epoch"]))
endMapData = dict(sorted(endMapData.items(), key=lambda item: item[1]["epoch"]))
# and then sort mapData by the scale
# this works cause Python sort is stable
overworldMapData = dict(sorted(overworldMapData.items(), key=lambda item: item[1]["scale"], reverse=True))
netherMapData = dict(sorted(netherMapData.items(), key=lambda item: item[1]["scale"], reverse=True))
endMapData = dict(sorted(endMapData.items(), key=lambda item: item[1]["scale"], reverse=True))



# We then go through the mapData dict and store in a diferent dict using topleft coord based on scale 4 as the key. This'll append to the list or create a list if there is none
# This one actually needs to be a dict cause we need to group the maps. Cool.


def createScale4Maps(mapData):
    scale4maps = defaultdict(list)
    for key, map in mapData.items():
        scale4maps[roundDown(map["anchor"], 4)].append(map)
    return scale4maps


# We then go through the dictionary and create an image based on each entry
# The images should be in their own dictionary. The key is the coords. The value is the image. No actually, it's fine if it's just a list. In fact we should just save them as they're made.
def createImages(scale4maps, dimension):
    if scale4maps is None:
        return
    for level4Coords, lists in tqdm(scale4maps.items(), desc="Creating map images and subimages"):
        # This iterates over every map in the scale 4 map area
        bigImage = Image.new( 'RGBA', (2048, 2048), (0, 0, 0, 0) )
        for map in lists:
            image = Image.new( 'RGBA', (128,128) )

            # Fills out the image pixel by pixel
            image.putdata(map["colors"])

            # Resize to proper size. So zoom 4 will be the 2048x2048 scale
            image = image.resize((128 * 2 ** map["scale"],) * 2, Image.NEAREST)
            bigImage.paste(image, normalizeAnchor(map["anchor"]))
        
        # Slices the image to make each zoom level
        for i in range(1, 5):
            for x in range(2 ** i):
                for y in range(2 ** i):
                    # x * (2048 / 2 ** i) This is the math for the left bound
                    # y * (2048 / 2 ** i) This is the math for the upper bound
                    # (x+1) * (2048 / 2 ** i) This is the math for the right bound
                    # (y+1) * (2048 / 2 ** i) This is the math for the lower bound
                    bounds = ((x * 2048 // 2 ** i), (y * 2048 // 2 ** i), ((x+1) * 2048 // 2 ** i), ((y+1) * 2048 // 2 ** i))

                    # Crop the specific region for the scale
                    image = bigImage.crop(bounds)

                    # If the selected area is empty, skip making the image
                    if image.getbbox() is None:
                        image.close()
                        continue

                    # Resize to the correct size for Leaflet
                    image = image.resize((128,) * 2, Image.NEAREST)
                    # Get the right image name:
                    folder, file = folderFileNames(level4Coords, scaleToZoom[i])
                    dir = os.path.join(sys.argv[2], dimension, f"{i}", f"{folder + x}")
                    if not os.path.isdir(dir):
                        os.makedirs(dir)
                    dir = os.path.join(dir, f"{file + y}.png")
                    image.save(dir)
                    image.close()
        
        # Saves the lowest level zoom
        folder, file = folderFileNames(level4Coords, 4)
        zoomFolder = scaleToZoom[4]
        dir = os.path.join(sys.argv[2], dimension, f"{zoomFolder}", f"{folder}")
        if not os.path.isdir(dir):
            os.makedirs(dir)
        bigImage = bigImage.resize((128,) * 2, Image.NEAREST)
        dir = os.path.join(dir, f"{file}.png")
        bigImage.save(dir)
        bigImage.close()


print("Overworld")
result = createScale4Maps(overworldMapData)
createImages(result, "overworld")

print("Nether")
result = createScale4Maps(netherMapData)
createImages(result, "nether")

print("End")
result = createScale4Maps(endMapData)
createImages(result, "end")