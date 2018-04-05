from rendertypes import *
from colour import Color
import sys
import math
from collisions import *


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
	
def phong():
	return 0

class ortocam:
	def __init__(self, position, direction, upVector, farPlane, width, heigth, stepx, stepy):
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
		laspix = self.basicOrig + (self.rightVector * width * self.stepx) + (self.upVector * heigth * self.stepy) 
		# print(self.rightVector, self.basicOrig, laspix)
	
	def parsePixel(self, coord, scene):
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
			return Color("white")
		else:
			# print("Hello")
			return mulCol(hit.material.dColor, scene.ambientLight)
	
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
	def parsePixel(self, coord, scene):
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
			return Color("white")
		else:
			return  mulCol(hit.material.dColor, scene.ambientLight)