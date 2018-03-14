from collisions import *
from types import *

#intersection tests:
#sphere - line tests
#2 intersections	
sphCenter = vector(6, 0 , 0)
sphRadius = 2
rayOr = vector(0,0,0)
rayDir = vector(1,0,0)
s = sphere(sphCenter, sphRadius)
r = ray(rayOr, rayDir)

result = raySphereColl(r, s)
expected = vector(4, 0, 0)

assert result.hitPoint == expected, "Assertion error expected: {} result: {}".format(expected, result)

#1 intersection
rayOr = vector(1, -1, 0)
rayDir = vector(0, 1, 0)
sphCenter = vector(0,0,0)
sphRadius = 1
s = sphere(sphCenter, sphRadius)
r = ray(rayOr, rayDir)

result = raySphereColl(r, s)
expected = vector(1, 0, 0)

assert result.hitPoint == expected, "Assertion error expected: {} result: {}".format(expected, result)

#no intersection
rayOr = vector(1, -1, 0)
rayDir = vector(0, -1, 0)
sphCenter = vector(0,0,0)
sphRadius = 1
s = sphere(sphCenter, sphRadius)
r = ray(rayOr, rayDir)

result = raySphereColl(r, s)
expected = None

assert result.hitPoint == expected, "Assertion error expected: {} result: {}".format(expected, result)

#plane - ray intersection
#there is intersection:
rayOr = vector(0, -1, 0)
rayDir = vector(0, 1, 0)

planePoint = vector(0, 1, 0)
planeNormal = vector(0, 1, 0)

r = ray(rayOr, rayDir)
p = plane(planePoint, planeNormal)

result = rayPlaneColl(r, p)
expected = vector(0, 1, 0)

assert result.hitPoint == expected, "Assertion error expected: {} result: {}".format(expected, result)

#there is no intersection, ray and plane are parallel
rayOr = vector(0, -1, 0)
rayDir = vector(1, 0, 0)

planePoint = vector(0, 1, 0)
planeNormal = vector(0, 1, 0)

r = ray(rayOr, rayDir)
p = plane(planePoint, planeNormal)

result = rayPlaneColl(r, p)
expected = None

assert result.hitPoint == expected, "Assertion error expected: {} result: {}".format(expected, result)

#intersection is behind ray origin
rayOr = vector(0, -1, 0)
rayDir = vector(0, -1, 0)

planePoint = vector(0, 1, 0)
planeNormal = vector(0, 1, 0)

r = ray(rayOr, rayDir)
p = plane(planePoint, planeNormal)

result = rayPlaneColl(r, p)
expected = None

assert result.hitPoint == expected, "Assertion error expected: {} result: {}".format(expected, result)


