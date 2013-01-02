#!/usr/bin/env python
import sys
import Image

COLORS = {"wall":(0,0,0,255), "teleporter":(255,0,0,255)}

#Open file
im = Image.open(sys.argv[1])
snake_map = im.load()

height = im.size[0]
length = im.size[1]

output = {}
output["dimensions"] = (height, length)

print >> sys.stderr, "Defined colors:", COLORS, "\nMap size:", output["dimensions"]
for k, v in COLORS.iteritems():
    output[k] = []
    current_line = 0
    for x in range(0,height):
        for y in range(0,length):
            p = snake_map[x,y]
            if p == v:
                output[k].append([x+1, y+1])

print(output)
