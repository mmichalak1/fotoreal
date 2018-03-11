from types import *
from collisions import *

# vec = vector(1, 1, 0)
# vec2 = vector(1,1,1)
# print(vec.getLength())
# print(vec.getLengthPow2())
# print(vec.nvector())
# print(vec * 2)
# print(2 * vec)
# print(vec//2)
# print(vec/2)
# vec.add(vec)
# print(vec)
# vec.sub(vec/2)
# print(vec)
# vec += vec
# print(vec)
# print(vec.scalar(vec2))
# print(vec.cross(vec2))
# print(vec.normalize())
# sph = sphere(vec,2)
# print(sph)
# pl = plane(vec,vec)
# print(pl)
# r1 = ray(vec,vec)
# print(r1)

#intersection tests:
#sphere - line tests
#2 intersections	
sphCenter = vector(6, 0 , 0)
sphRadius = 2
rayOr = vector(0,0,0)
rayDir = vector(1,0,0)
s = sphere(sphCenter, sphRadius)
r = ray(rayOr, rayDir)

result = rayShpereColl(r, s)
expected = vector(4, 0, 0)

assert result == expected, "Assertion error expected: {} result: {}".format(expected, result)

#1 intersection
rayOr = vector(1, -1, 0)
rayDir = vector(0, 1, 0)
sphCenter = vector(0,0,0)
sphRadius = 1
s = sphere(sphCenter, sphRadius)
r = ray(rayOr, rayDir)

result = rayShpereColl(r, s)
expected = vector(1, 0, 0)

assert result == expected, "Assertion error expected: {} result: {}".format(expected, result)


#no intersection
rayOr = vector(1, -1, 0)
rayDir = vector(0, -1, 0)
sphCenter = vector(0,0,0)
sphRadius = 1
s = sphere(sphCenter, sphRadius)
r = ray(rayOr, rayDir)

result = rayShpereColl(r, s)
expected = None

assert result == expected, "Assertion error expected: {} result: {}".format(expected, result)