import gzip

file = "map_0.dat"
map = gzip.open(file, 'rb')
file_content = map.read(1)
count = 0
while file_content != b'':
    print(file_content)
    file_content = map.read(1)