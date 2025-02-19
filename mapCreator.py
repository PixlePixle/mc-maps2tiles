import parser
import math
from PIL import Image
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

scaleDict = {0: 128,
             1: 256,
             2: 512,
             3: 1024,
             4: 2048}



# So with the scale, we can be very inefficient.
# With each layer, we have to make 2^scale images along each axis
# scale 0: 1(1x1) 256x256 image, 1: 4(2x2) 256x256 images, 2: 16(4x4) 256x256 images, 3: 64(8x8) 256x256 images, 4:(16x16) 256 256x256 images
# This is because each tile is 256x256 in Leaflet. Each zoom level splits the tiles into 2. Or something like that.
# I need to try leafleft before I understand

# Getting values from the parser
mapData = parser.parse(sys.argv[1])
scale = mapData["data"]["scale"]
banners = mapData["data"]["banners"]
frames = mapData["data"]["frames"]
zCenter = mapData["data"]["zCenter"]
xCenter = mapData["data"]["xCenter"]

# Despite the scales, the maps are still 128x128. Rather, it is the amount of area it covers.
# Create a new Image object
image = Image.new( 'RGBA', (128, 128)) 

# Converts from Minecraft map color index to actual RGB
colors = mapData["data"]["colors"]
mapImage = [allColors[a] for a in colors]

# Fills out the image pixel by pixel
image.putdata(mapImage)

# Saves the image in the same location as the file as a png
length = len(sys.argv[1])
image.save(sys.argv[1][0:length-4] + ".png")