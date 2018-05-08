from rendertypes import *
from colour import Color
import sys
import math
from collisions import *

phong = True

def addColor(colors):
	red = 0.
	green = 0.
	blue = 0.
	for color in colors:
		red += color.red
		green += color.green
		blue += color.blue
	col = Color()
	col.red = max(min(red, 1.), 0.)
	col.green = max(min(green, 1.), 0.)
	col.blue = max(min(blue, 1.), 0.)
	return col
	
def mulCol(c1, c2):
	return Color(rgb=(c1.red * c2.red, c1.green * c2.green, c1.blue * c2.blue))
	
def spericalTexture(hit):
	localHitPoint = (hit.hitPoint - hit.hitObj.center)/hit.hitObj.radius
	u= math.atan(localHitPoint.x/localHitPoint.z)
	v = 1 - math.acos(localHitPoint.y)/math.pi
	if(u<0):
		u += math.pi*2
	u /= (2*math.pi)
	
	#print("({},{})".format(u,v))
	return hit.hitObj.material.texture.getTexturePoint(u,v)
		
def rectTexture(hit):
	localHitPoint = hit.hitPoint - hit.hitObj.center
	u = localHitPoint.x % hit.material.texture.width-1
	v = localHitPoint.z % hit.material.texture.height-1
	return hit.material.texture.getRawPoint(u, v)
		
def phong(hit, Iray, scene, rec):
	color = Color(rgb = (0.0,0.0,0.0))
	
	if rec > 0:
		if hit.material.mirror:
			reflVec = Iray.direction.normalize() - (2.0 * hit.normal.normalize() * (hit.normal.normalize() * Iray.direction.normalize()))
			reflRey = ray(hit.hitPoint, reflVec.normalize())
			minDistance = sys.maxsize
			reflHit = None
			for obj in scene.objects:
				if hit.hitObj != obj: 
					tmpHit = reflRey.isColliding(obj)
					if tmpHit != None
						distance = (tmpHit.hitPoint - hit.hitPoint).getLength()
						if ( distance < minDistance):
							reflHit = tmpHit
							minDistance = distance
			if reflHit != None:
				color = addColor((phong(reflHit,reflRey, scene,rec-1), color))
	if hit.material.refraction > 1:
		pass
	for light in scene.lights: 
		hitToLight = (light.position - hit.hitPoint)
		rayTolight = ray(hit.hitPoint, hitToLight.normalize(), hitToLight.getLength())
		directLight = True
		for obj in scene.objects:
			if hit.hitObj != obj: 
				if rayTolight.isColliding(obj) != None:
					directLight = False
		if directLight:
			reflectionVec =(hit.normal.normalize() * (hit.normal.normalize() *rayTolight.direction.normalize()) * 2.0) - rayTolight.direction.normalize() 
			s = Iray.direction.normalize() * reflectionVec
			s = (s)**hit.material.refl
			s *= hit.material.specK
			specCol = Color(rgb = (light.color.red * s,light.color.green * s, light.color.blue * s))
			diff = rayTolight.direction.normalize() * hit.normal
			if(diff <0):
				diff = 0
			diff *= hit.material.diffK
			diffCol = Color(rgb = (light.color.red * diff,light.color.green * diff, light.color.blue * diff))
			color = addColor((specCol,color))
			color = addColor((color,diffCol))
	ambCol = Color(rgb = (scene.ambientLight.red * hit.material.ambK,scene.ambientLight.green * hit.material.ambK, scene.ambientLight.blue * hit.material.ambK))
	color = addColor((color,ambCol))
	if(hit.material.texture != None):
		if hit.material.texture.type == 0:
			return mulCol(spericalTexture(hit), color)
		elif hit.material.texture.type == 1:
			return mulCol(rectTexture(hit), color)
	else:
		return color
	

class ortocam:
	def __init__(self, position, direction, upVector, farPlane, width, heigth, stepx, stepy, defcol = Color("white")):
		self.position = position
		self.direction = direction
		self.upVector = upVector
		self.rightVector = upVector.cross(direction)
		self.basicOrig = vector(self.position)
		self.basicOrig -= (upVector.normalize().cross(direction.normalize()))*(width / 2)
		self.basicOrig += upVector.normalize() * (heigth/ 2)
		self.stepx = stepx
		self.stepy = stepy
		self.farPlane = farPlane
		self.defcol = defcol
		
	def parsePixel(self, coord, scene, rec):
		rayOrig = vector(self.basicOrig)
		rayOrig += self.rightVector * self.stepx * coord[0]
		rayOrig -= self.upVector * self.stepy * coord[1]
		# print(rayOrig)
		r = ray(rayOrig, self.direction)
		minDistance = self.farPlane
		hit = None
		# print(objects)
		for obj in scene.objects:
			tmp = r.isColliding(obj)
			if tmp != None:
				distance = (tmp.hitPoint - r.origin).getLength()
				if ( distance < minDistance):
					hit = tmp
					minDistance = distance
		if (hit == None):
			return self.defcol
		else:
			# print("Hello")
			return phong(hit, r,scene, rec)
	
class perspectiveCam:
	def __init__(self, position, direction, upVector, farPlane, nearPlane, fov, width, height, stepx, stepy):
		self.position = position
		self.direction = direction
		self.upVector = upVector
		self.nearPlane = nearPlane
		self.farPlane = farPlane
		self.fov = fov
		self.width = width
		self.height = height
		self.stepx = stepx
		self.stepy = stepy
		self.basicOrig = (position+(direction.normalize()*self.getProjectionDistance())) - ((upVector.normalize().cross(direction.normalize()))*(width / 2)) + (upVector.normalize() * (height/ 2))
		# print(self.basicOrig)
		# print((upVector.normalize().cross(direction.normalize())))
	def getProjectionDistance(self):
		distance = (math.tan(math.radians(self.fov/2))) * self.width/2
		return distance
	def parsePixel(self, coord, scene, rec):
		rayOrig = vector(self.basicOrig.x, self.basicOrig.y, self.basicOrig.z)
		rayOrig += self.upVector.normalize().cross(self.direction.normalize()) * (self.stepx * coord[0])
		rayOrig -= self.upVector.normalize() * self.stepy * coord[1]
		r = ray(self.position, (rayOrig - self.position).normalize())
		minDistance = self.farPlane
		hit = None
		# print(objects)
		for obj in scene.objects:
			tmp = r.isColliding(obj)
			if tmp != None:
				distance = (tmp.hitPoint - r.origin).getLength()
				if ( distance < minDistance):
					hit = tmp
					minDistance = distance
		if (hit == None):
			return Color("Black")
		else:
			return phong(hit,r,scene, rec)
