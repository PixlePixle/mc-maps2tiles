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

def folderFileNames(startCoords, scale):
    return tuple( value // scaleDict[scale] for value in startCoords)

# I need a sorting funcion for how I want to sort it as well. Whether that's time, newer maps always on top, or size, smaller maps always on top.

# Everything above is base setup for processing
# -----------------------------------------------
# Everything below is for image processing based on above data
# What I want to do is create the lowest zoom and go in.
# Lowest image, create 
# This involves splitting everything above zoom 0.
# So for the largest scale keeping track of 256 left corners.
# We can split using Image.crop: https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.crop

# So with the scale, we can be very inefficient.
# With each layer, we have to make 2^scale images along each axis
# scale 0: 1(1x1) 128x128 image, 1: 4(2x2) 128x128 images, 2: 16(4x4) 128x128 images, 3: 64(8x8) 128x128 images, 4:(16x16) 256 128x128 images
# This is because each tile is set to be 128x128 in Leaflet (Default was 256). Each zoom level splits the tiles into 4 (2^2). Or something like that.
# The math for this in a for loop:
# for i in range((2 ** scale) ** 2): # This'll return the total number of images. Maybe split into nested for loop? range(2**scale)
# X, -Left +Right
# Y, -Down +Up
# Folder is Zoom Level
# scale: 0 = 4
# scale: 1 = 3
# scale: 2 = 2
# scale: 3 = 1
# scale: 4 = 0
# The solution is (4 - scale) to get the correct folder name
# Nested Folder is X, Left Right
# scale 0: anchor.x/64 = Folder
# scale 1: anchor.x/192 = Folder
# scale 2: anchor.x/448 = Folder
# scale 3: anchor.x/960 = Folder
# scale 4: anchor.x/1984 = Folder
# Image Name is Y, Up Down
# scale 0: anchor.z/64 = File Name
# scale 1: anchor.z/192 = File Name
# scale 2: anchor.z/448 = File Name
# scale 3: anchor.z/960 = File Name
# scale 4: anchor.z/1984 = File Name

# Get all the maps in the folder. Sort them by size, highest zoom to lowest. Skip all non player maps.
# Create images using all the scale 4 maps. Making them to actual coverage size. In the instance a map covers the same, get the time of the map modified. Newest map written on top of the old map. Don't replace it, that way we can preserve old data if new map doesn't cover it all
# https://docs.python.org/3/library/os.path.html#os.path.getmtime
# Then proceed through the scale3, adding them onto the scale 4 maps if the bounds are within topleft + 1024.
# Make a new image the size of scale 4 if one doesn't exist for the area and then put in correct position.
# Repeat for scale 2, 1, and 0.
# That'll give us the base images to use to make tiles for everything else.
# We then will cut up the images as needed for every zoom and then resize them to the correct size of 128x128

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

# I should probably not get the map directory instead but keep it as filenames. I need the info from them (time).
# or not... apparently iterating over dictionaries iterates over keys and not values
# Though doing mapData[key] could add slowdowns
# That's why you iterate with `for key,value in dict.items()`
# Iterates over the source directory files and selects what should be player maps only.
mapData = {}
for filename in tqdm(filenames, desc=('Picking player maps')):
    temp = parser.parse(filename)
    temp = temp["data"]
    if temp["unlimitedTracking"] == 0:
        # colors = temp["colors"]
        temp["colors"] = [allColors[a] for a in temp["colors"]]
        temp["epoch"] = os.path.getmtime(filename)
        temp["anchor"] = [temp["xCenter"] - (64 * 2 ** temp["scale"]) + 64, temp["zCenter"] - (64 * 2 ** temp["scale"]) + 64]
        mapData[filename] = temp
print(f"Player maps count: {len(mapData)}")

# It might be bad to assume that dicts are always ordered... Additionally, since I have the epoch stored with the data, it's no longer necessary to keep filename.
# I should probably change this to a list

# sort mapData by time modified
mapData = dict(sorted(mapData.items(), key=lambda item: item[1]["epoch"]))
# and then sort mapData by the scale
# this works cause Python sort is stable
mapData = dict(sorted(mapData.items(), key=lambda item: item[1]["scale"], reverse=True))



# for map in mapData:
#     print("Filename: " + str(map) + "Scale: " + str(mapData[map]["scale"]) + " Epoch: " + str(mapData[map]["epoch"]))


# We then go through the mapData dict and store in a diferent dict using topleft coord based on scale 4 as the key. This'll append to the list or create a list if there is none
# This one actually needs to be a dict cause we need to group the maps. Cool.
scale4maps = defaultdict(list)
for key, map in mapData.items():
    scale4maps[roundDown(map["anchor"], 4)].append(map)


# We then go through the dictionary and create an image based on each entry
# The images should be in their own dictionary. The key is the coords. The value is the image. No actually, it's fine if it's just a list. In fact we should just save them as they're made.

for startCoords, lists in scale4maps.items():
    print(str(startCoords))
    folder, file = folderFileNames(startCoords, 4)
    # This iterates over every map in the scale 4 map area
    bigImage = Image.new( 'RGBA', (2048, 2048), (0, 0, 0, 0) )
    for map in lists:
        image = Image.new( 'RGBA', (128,128) )

        # Fills out the image pixel by pixel
        image.putdata(map["colors"])

        # Resize to proper size. So zoom 4 will be the 2048x2048 scale
        image = image.resize((128 * 2 ** mapData[key]["scale"],) * 2, Image.NEAREST)
        bigImage.paste(image, normalizeAnchor(map["anchor"]))
        print("Anchor: " + str(map["anchor"]) + " Normalized: " + str(normalizeAnchor(map["anchor"])))
    
    # Add slicing here
    for i in range(1, 5):
        for x in range(2 ** i):
            # THE MATH FOR DIR AND IMAGE NAME IS WRONG
            dir = sys.argv[2] + f"{i}/{(startCoords[0] // 2 ** i) // scaleDict[scaleToZoom[i]]}"
            if not os.path.isdir(dir):
                os.makedirs(dir)
            for y in range(2 ** i):
                print("x: " + str(x) + ", y: " + str(y))
                # x * (2048 / 2 ** i) This is the math for the left bound
                # y * (2048 / 2 ** i) This is the math for the upper bound
                # (x+1) * (2048 / 2 ** i) This is the math for the right bound
                # (y+1) * (2048 / 2 ** i) This is the math for the lower bound
                bounds = ((x * 2048 // 2 ** i), (y * 2048 // 2 ** i), ((x+1) * 2048 // 2 ** i), ((y+1) * 2048 // 2 ** i))

                image = bigImage.crop(bounds)
                image = image.resize((128,) * 2, Image.NEAREST)
                # Get the right image name:
                
                image.save(dir + f"/{(startCoords[1] // 2 ** i) // scaleDict[scaleToZoom[i]]}.png")
                image.close()
                
    
    # Saves the lowest level zoom
    zoomFolder = scaleToZoom[4]
    dir = sys.argv[2] + f"{zoomFolder}/{folder}"
    if not os.path.isdir(dir):
        os.makedirs(dir)
    bigImage = bigImage.resize((128,) * 2, Image.NEAREST)
    bigImage.save(dir + f"/{file}.png")
    
    bigImage.close()
    print("-----")


# count = 0
# # For now, just makes images from the player maps
# for key in mapData:
#     image = Image.new( 'RGBA', (128, 128)) 

#     # Fills out the image pixel by pixel
#     image.putdata(mapData[key]["colors"])

#     # So zoom 4 will be the 2048x2048 scale
#     image = image.resize((128 * 2 ** mapData[key]["scale"],) * 2, Image.NEAREST)

#     # Saves the image in the same location as the file as a png
#     image.save(sys.argv[2] + f"/{count}.png")
#     count = count + 1











# Code to make a single image (reference)
# ---------------------------------------------
# # Get these, put them in a list or dict or something
# # Getting values from the parser
# mapData = parser.parse(sys.argv[1])
# scale = mapData["data"]["scale"]
# banners = mapData["data"]["banners"]
# frames = mapData["data"]["frames"]
# zCenter = mapData["data"]["zCenter"]
# xCenter = mapData["data"]["xCenter"]
# print(xCenter, zCenter)

# # I don't remember what this makes, I just made it. I believe the goal of this is to shift the origin to start from the top left corner for all future calculations
# # Calculates the topleft coord from the center. This is done because each map expands down and right. Therefore, no matter the zoom, maps in the same section have the same top left corner.
# # anchor = [xCenter - (64 * 2 ** scale) + 64, zCenter - (64 * 2 ** scale)]
# anchor = [xCenter - (64 * 2 ** scale) + 64, zCenter - (64 * 2 ** scale) + 64]
# print(anchor)

# # The z center moves according to the scale. Cause each time, it doubles the length and height.
# # scale 0: 0, 0
# # 1: 64, 64
# # 2: 192, 192
# # 3: 448, 448
# # 4: 960, 960
# # This means that from 0->1 + 64, 1->2, + 128, 2->3 + 256, 3->4 + 512
# # That is how we get the math 64 * 2 ** scale


# # All Minecraft Maps are 128x128 no matter the scale. Rather with scale, each pixel represents aan average of a bigger area of blocks. Max zoom, 1 pixel = 16x16 blocks
# # Create a new Image object
# image = Image.new( 'RGBA', (128, 128)) 

# # Converts from Minecraft map color index to actual RGB
# colors = mapData["data"]["colors"]
# mapImage = [allColors[a] for a in tqdm(colors, desc='Writing Image')]

# # Fills out the image pixel by pixel
# image.putdata(mapImage)

# # So zoom 4 will be the 2048x2048 scale
# image = image.resize((128 * 2 ** scale,) * 2, Image.NEAREST)

# # Saves the image in the same location as the file as a png
# length = len(sys.argv[1])
# image.save(sys.argv[1][0:length-4] + ".png")