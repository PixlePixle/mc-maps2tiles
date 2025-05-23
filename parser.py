import gzip
import struct
import sys
from pprint import pprint

# Things to note, Python just uses more general types
# Therefore, int can be used for Byte, Short, Int, and Long
# And float can be used for Float, and Double
# Arrays are just arrays (using ndarray?)
# Compounds are dicts
# Lists are lists maybe? So basically this is like the C# list. List<tagID>. All the values within DO NOT have names.
id = {
    10: 'Compound',
    0: 'End',
    1: 'Byte',
    2: 'Short',
    3: 'Int',
    4: 'Long',
    5: 'Float',
    6: 'Double',
    8: 'String',
    9: 'List', 
    7: 'Byte_Array',
    11: 'Int_Array',
    12: 'Long_Array',
}

# Primitives
def Byte():
    return int.from_bytes(map.read(1), byteorder="big", signed=True)

def Short():
    return int.from_bytes(map.read(2), byteorder="big", signed=True)

def Int():
    return int.from_bytes(map.read(4), byteorder="big", signed=True)

def Long():
    return int.from_bytes(map.read(8), byteorder="big", signed=True)

def Float():
    return struct.unpack('!f', map.read(4))[0]


def Double():
    return struct.unpack('!d', map.read(8))[0]

def String():
    length = int.from_bytes(map.read(2), byteorder="big", signed=False)
    return map.read(length).decode()

# List
def List():
    list = []

    # Gets the type
    tag = int.from_bytes(map.read(1), byteorder="big", signed=False)
    if tag not in id:
        print(f"Unknown tag: {tag}")
        return list
    tag = id[tag]

    # Gets the length of the list
    length = int.from_bytes(map.read(4), byteorder="big", signed=True)

    # Returns a list of objects
    for i in range(length):
        match tag:
            case "Compound":
                returnObject = Compound()
                list.append(returnObject)
            case "Byte":
                returnObject = Byte()
                list.append(returnObject)
            case "Short":
                returnObject = Short()
                list.append(returnObject)
            case "Int":
                returnObject = Int()
                list.append(returnObject)
            case "Long":
                returnObject = Long()
                list.append(returnObject)
            case "Float":
                returnObject = Float()
                list.append(returnObject)
            case "Double":
                returnObject = Double()
                list.append(returnObject)
            case "String":
                returnObject = String()
                list.append(returnObject)
            case "Byte_Array":
                returnObject = Byte_Array()
                list.append(returnObject)
            case "Int_Array":
                returnObject = Int_Array()
                list.append(returnObject)
            case "Long_Array":
                returnObject = Long_Array()
                list.append(returnObject)
    return list


# Byte is correctly implemented. Unsure of the other arrays.

# Arrays
def Byte_Array():
    size = int.from_bytes(map.read(4), byteorder="big", signed=True)
    array = []
    for i in range(size):
        array.append(int.from_bytes(map.read(1), byteorder="big", signed=True))
    return array

def Int_Array():
    size = int.from_bytes(map.read(4), byteorder="big", signed=True)
    array = []
    for i in range(size):
        array.append(int.from_bytes(map.read(4), byteorder="big", signed=True))
    return array

def Long_Array():
    size = int.from_bytes(map.read(4), byteorder="big", signed=True)
    array = []
    for i in range(size):
        array.append(int.from_bytes(map.read(8), byteorder="big", signed=True))
    return array
    
# Compound
def Compound():
    # This should be a recursive function. It returns a dictionary. It returns whenever the end tag is encountered. This calls every other function. It adds it to itself's dictionary
    self = {}
    while 1 == 1:
        file_content = map.read(1)

        # Ends the loop at end of fileLocation
        if file_content == b'':
            break

        # Gets the tag
        tag = int.from_bytes(file_content, byteorder="big", signed=False)
        if tag not in id:
            print(f"Unknown tag: {tag}")
            continue
        tag = id[tag]

        # Returns if the next tag is an end tag
        if tag == "End":
            break

        # Gets the name of the component to put
        nameLength = int.from_bytes(map.read(2), byteorder="big", signed=False)
        name = map.read(nameLength).decode()

        match tag:
            case "Compound":
                returnObject = Compound()
                self[name] = returnObject
            
            case "Byte":
                returnObject = Byte()
                self[name] = returnObject

            case "Short":
                returnObject = Short()
                self[name] = returnObject

            case "Int":
                returnObject = Int()
                self[name] = returnObject

            case "Long":
                returnObject = Long()
                self[name] = returnObject

            case "Float":
                returnObject = Float()
                self[name] = returnObject

            case "Double":
                returnObject = Double()
                self[name] = returnObject

            case "String":
                returnObject = String()
                self[name] = returnObject

            case "List":
                returnObject = List()
                self[name] = returnObject

            case "Byte_Array":
                returnObject = Byte_Array()
                self[name] = returnObject
            case "Int_Array":
                returnObject = Int_Array()
                self[name] = returnObject
            case "Long_Array":
                returnObject = Long_Array()
                self[name] = returnObject
    return self

map = None

# Defining main parsing function
# TODO: Update this to check whether the file is compressed or not and
# act accordingly.
def parse(fileLocation):
    global map
    map = gzip.open(fileLocation, 'rb')
    # Burn the initial 0x0a (10) tag
    map.read(1)
    # The root compound tag. Should always be the root. Has no name. 
    # Therefore, this will only read the two bytes for the name length (0)
    nameLength = int.from_bytes(map.read(2), byteorder="big", signed=False)
    name = map.read(nameLength).decode()
    root = Compound()
    map.close()
    return root


# Using the special variable 
# __name__
if __name__=="__main__":
    pprint(parse(sys.argv[1]))

