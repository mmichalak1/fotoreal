import rendertypes as rt
import math
EPS = 1e-6

#bazowane w wzorze ax^2 + bx + c gdzie:
#v = s.center - p.origin
#a = 1
#b = 2 * ray.origin * ray.direction
#c = ray.origin^2 - sphere.radius^2
#liczymy delte ze wzoru: d = b^2 - 4ac
def raySphereColl(r, s):
	#print(r, s)
	if (not isinstance(r, rt.ray) or not isinstance(s, rt.sphere)):
		print("ERROR: r or s is not ray or sphere")
		return None
	a = r.origin - s.center
	b = 2 * r.direction * a
	c = a * a - s.radius**2
	delta = b * b - (4 * c)
	# print("DEBUG: a={} b={} c={} delta={}".format(a,b,c,delta))
	if delta < 0:
		return None
	if abs(delta) < EPS:
		root = -b / 2
		if root < 0:
			return None
		else:
			return rt.hit(r, r.origin + r.direction * root, s.color, root)
	rootA = (-b - math.sqrt(delta))/2
	rootB = (-b + math.sqrt(delta))/2
	if rootA < 0 and rootB < 0:
		return None
	if rootA < 0:
		print("WARNING: inisde a sphere")
		return rt.hit(r, r.origin + r.direction * rootB, s.color, rootB)
	if rootB < 0:
		print("WARNING: inisde a sphere")
		return rt.hit(r, r.origin + r.direction * rootA, s.color, rootA)
	root = min(rootA, rootB)
	return rt.hit(r, r.origin + r.direction * root, s.color, rootB)

#t = (d - N dot X) / (N dot V)
#d = p.normal dot p.point
#N = p.normal
#X = r.origin
#V = r.direction
def rayPlaneColl(r, p):
	if (not isinstance(r, rt.ray) or not isinstance(p, rt.plane)):
		print("ERROR: r or s is not ray or plane")
		return None
	if abs(r.direction * p.normal) < EPS:
		return None
	d = p.normal * p.point
	t = (d - p.normal * r.origin) / (p.normal * r.direction)
	# print("DEBUG: t={}".format(t))
	if t < 0:
		return None
	# print("DEBUG: t={}".format(t))
	return rt.hit(r, r.origin + r.direction * t, p.color, t)
	
def rayTriangleColl(r, t):
	p = rt.plane(t.v1, t.direction)
	coll = r.isColliding(p)
	if(coll == None):
		return None
	hit = coll.hitPoint
	fa = t.v1 - hit
	fb = t.v2 - hit
	fc = t.v3 - hit
	
	cross = fa.cross(fb)
	if cross * t.direction < 0:
		return None
	
	cross = fb.cross(fc)
	if cross * t.direction < 0:
		return None
	
	cross = fc.cross(fa)
	if cross * t.direction < 0:
		return None
	
	# print("well hello there")
	return rt.hit(r, coll.hitPoint, t.material, coll.result)
	
def rayMeshColl(r,m):
	hit = None
	minDistance = 1000000000000
	for obj in m.triangles:
		tmp = rayTriangleColl(r, obj)
		if tmp != None:
			distance = (tmp.hitPoint - r.origin).getLength()
			if ( distance < minDistance):
				hit = tmp
				minDistance = distance
	return hit