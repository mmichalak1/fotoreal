from types import *


#bazowane w wzorze ax^2 + bx + c gdzie:
#v = s.center - p.origin
#a = 1
#b = 2 * ray.origin * ray.direction
#c = ray.origin^2 - sphere.radius^2
#liczymy delte ze wzoru: d = b^2 - 4ac
def rayShpereColl(r, s):
	if (not isinstance(r, ray) or not isinstance(s, sphere)):
		print("ERROR: r or s is not ray or sphere")
		return None
	a = r.origin - s.center
	b = 2 * r.direction * a
	c = a * a - s.radius**2
	delta = b * b - (4 * c)
	# print("DEBUG: a={} b={} c={} delta={}".format(a,b,c,delta))
	if delta < 0:
		return None
	if delta == 0:
		root = -b / 2
		if root < 0:
			return None
		else:
			return r.origin + r.direction * root
	rootA = (-b - math.sqrt(delta))/2
	rootB = (-b + math.sqrt(delta))/2
	if rootA < 0 and rootB < 0:
		return None
	if rootA < 0:
		return r.origin + r.direction * rootB
	if rootB <0:
		return r.origin + r.direction * rootA
	return r.origin + r.direction * min(rootA, rootB)