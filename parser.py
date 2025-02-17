import gzip

file = "map_0.dat"
map = gzip.open(file, 'rb')

id = {
    0: 'End',
    1: 'Byte',
    2: 'Short',
    3: 'Int',
    4: 'Long',
    5: 'Float',
    6: 'Double',
    7: 'Byte_Array',
    8: 'String',
    9: 'List',
    10: 'Compound',
    11: 'Int_Array',
    12: 'Long_Array',

}

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

    print(tag)
    nameLength = int.from_bytes(map.read(2), "big")
    if nameLength != 0:
        name = map.read(nameLength)
        print(name)
