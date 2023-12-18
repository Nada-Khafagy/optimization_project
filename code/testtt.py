import math
l = []
for deg in range(360) :
    l.append( int(128 + (64 * math.sin((deg * math.pi) / 180)) ))
print(len(l))