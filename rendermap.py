#!/usr/bin/env python
import sys

CHARS = {"wall":"X", "empty":" ", "potato_bomb":"?"}

#Open file
snake_map = sys.stdin.read().splitlines()

#Validate file
height = len(snake_map)
length = len(snake_map[0])

#File must be a rectangle.
for l in snake_map:
    if len(l) != length:
        sys.exit("Map is not rectangular. Map should not contain multi-byte characters.")
print >> sys.stderr, "Reading map file, %d by %d." % (height, length)

output = {}
output["dimensions"] = (height, length)

print >> sys.stderr, "Defined characters:", CHARS
for k, v in CHARS.iteritems():
    if k != "empty":
        output[k] = []
        current_line = 0
        for l in snake_map:
            current_col = 0
            for c in l:
                if c == v:
                    output[k].append([current_line+1, current_col+1])
                current_col += 1
            current_line += 1

print(output)
print >> sys.stderr, snake_map
