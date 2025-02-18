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
    nameLength = int.from_bytes(map.read(2), byteorder="big", signed=False)
    name = map.read(nameLength).decode()
    return name, int.from_bytes(map.read(1))

def Short():
    nameLength = int.from_bytes(map.read(2), byteorder="big", signed=False)
    name = map.read(nameLength).decode()
    return name, int.from_bytes(map.read(2))

def Int():
    nameLength = int.from_bytes(map.read(2), byteorder="big", signed=False)
    name = map.read(nameLength).decode()
    return name, int.from_bytes(map.read(4))

def Long():
    nameLength = int.from_bytes(map.read(2), byteorder="big", signed=False)
    name = map.read(nameLength).decode()
    return name, int.from_bytes(map.read(8))

def Float():
    nameLength = int.from_bytes(map.read(2), byteorder="big", signed=False)
    name = map.read(nameLength).decode()
    return name, float.fromhex(map.read(4).hex())

def Double():
    nameLength = int.from_bytes(map.read(2), byteorder="big", signed=False)
    name = map.read(nameLength).decode()
    return name, float.fromhex(map.read(8).hex())

def String():
    nameLength = int.from_bytes(map.read(2), byteorder="big", signed=False)
    name = map.read(nameLength).decode()
    length = int.from_bytes(map.read(2), byteorder="big", signed=False)
    return name, map.read(length).decode()

# TODO: Implement List
# List
def List():
    nameLength = int.from_bytes(map.read(2), byteorder="big", signed=False)
    name = map.read(nameLength).decode()
    tag = int.from_bytes(map.read(1))
    length = int.from_bytes(map.read(4))
    list = []



# Arrays
def Byte_Array():
    nameLength = int.from_bytes(map.read(2), byteorder="big", signed=False)
    name = map.read(nameLength).decode()
    size = int.from_bytes(map.read(4))
    array = []
    for i in range(size):
        array.append(int.from_bytes(map.read(1)))
    return name, array

def Int_Array():
    nameLength = int.from_bytes(map.read(2), byteorder="big", signed=False)
    name = map.read(nameLength).decode()
    size = int.from_bytes(map.read(4))
    array = []
    for i in range(size):
        array.append(int.from_bytes(map.read(4)))
    return name, array

def Long_Array():
    nameLength = int.from_bytes(map.read(2), byteorder="big", signed=False)
    name = map.read(nameLength).decode()
    size = int.from_bytes(map.read(4))
    array = []
    for i in range(size):
        array.append(int.from_bytes(map.read(8)))
    return name, array
    
# Compound
def Compound():
    # Get name of itself
    nameLength = int.from_bytes(map.read(2), byteorder="big", signed=False)
    name = map.read(nameLength).decode()
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

        match tag:
            case "Compound":
                returnName, returnObject = Compound()
                self[returnName] = returnObject

            case "End":
                return name, self
            
            case "Byte":
                returnName, returnObject = Byte()
                self[returnName] = returnObject

            case "Short":
                returnName, returnObject = Short()
                self[returnName] = returnObject

            case "Int":
                returnName, returnObject = Int()
                self[returnName] = returnObject

            case "Long":
                returnName, returnObject = Long()
                self[returnName] = returnObject

            case "Float":
                returnName, returnObject = Float()
                self[returnName] = returnObject

            case "Double":
                returnName, returnObject = Double()
                self[returnName] = returnObject

            case "String":
                returnName, returnObject = String()
                self[returnName] = returnObject

            case "Byte_Array":
                returnName, returnObject = Byte_Array()
                self[returnName] = returnObject
            case "Int_Array":
                returnName, returnObject = Int_Array()
                self[returnName] = returnObject
            case "Long_Array":
                returnName, returnObject = Long_Array()
                self[returnName] = returnObject

        pprint.pp(self)
    return name, self

# Defining main function
def main():
    root = {}
    map.read(1)
    returnName, returnObject = Compound()
    root[returnName] = returnObject
    pprint.pp(root)


# Using the special variable 
# __name__
if __name__=="__main__":
    main()

