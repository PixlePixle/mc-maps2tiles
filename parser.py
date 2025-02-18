import gzip
import pprint

file = "map_0.dat"
map = gzip.open(file, 'rb')

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
    # GETTING NAME USED TO BE HERE
    return int.from_bytes(map.read(1))

def Short():
    # GETTING NAME USED TO BE HERE
    return int.from_bytes(map.read(2))

def Int():
    # GETTING NAME USED TO BE HERE
    return int.from_bytes(map.read(4))

def Long():
    # GETTING NAME USED TO BE HERE
    return int.from_bytes(map.read(8))

def Float():
    # GETTING NAME USED TO BE HERE
    return float.fromhex(map.read(4).hex())

def Double():
    # GETTING NAME USED TO BE HERE
    return float.fromhex(map.read(8).hex())

def String():
    # GETTING NAME USED TO BE HERE
    length = int.from_bytes(map.read(2), byteorder="big", signed=False)
    return map.read(length).decode()

# List
def List():
    list = []

    # Gets the tag
    tag = int.from_bytes(map.read(1))
    if tag not in id:
        print(f"Uknown tag: {tag}")
        return list
    tag = id[tag]

    # Gets the length of the list
    length = int.from_bytes(map.read(4))

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


# The array's are improperly implemented for everything besides Byte.
# The arrays need to get the tag objects, they aren't simply the values. That would be a list.
# This shouldn't be relevant for maps as they don't use any arrays except byte arrays but something to keep in mind.

# Arrays
def Byte_Array():
    # GETTING NAME USED TO BE HERE
    size = int.from_bytes(map.read(4))
    array = []
    for i in range(size):
        array.append(int.from_bytes(map.read(1)))
    return array

def Int_Array():
    # GETTING NAME USED TO BE HERE
    size = int.from_bytes(map.read(4))
    array = []
    for i in range(size):
        array.append(int.from_bytes(map.read(4)))
    return array

def Long_Array():
    # GETTING NAME USED TO BE HERE
    size = int.from_bytes(map.read(4))
    array = []
    for i in range(size):
        array.append(int.from_bytes(map.read(8)))
    return array
    
# Compound
def Compound():
    # GETTING NAME USED TO BE HERE
    # This should be a recursive function. It returns a dictionary. It returns whenever the end tag is encountered. This calls every other function. It adds it to itself's dictionary
    self = {}
    while 1 == 1:
        file_content = map.read(1)

        # Ends the loop at end of file
        if file_content == b'':
            break

        # Gets the tag
        tag = int.from_bytes(file_content, "big")
        if tag not in id:
            print(f"Uknown tag: {tag}")
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

# Defining main function
def main():
    # Burn the initial 0x0a tag
    map.read(1)
    # The root compound tag. Should always be the root. Has no name. 
    # Therefore, this will only read the two bytes for the name length (0)
    nameLength = int.from_bytes(map.read(2), byteorder="big", signed=False)
    name = map.read(nameLength).decode()
    root = Compound()

    pprint.pp(root)
    map.close()


# Using the special variable 
# __name__
if __name__=="__main__":
    main()

