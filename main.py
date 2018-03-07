import math


class vector:
	def __init__(self, a, b, c):
		self.x = a
		self.y = b
		self.z = c
	def getLengthPow2(self):
		result = 0
		result += self.x**2 
		result += self.y**2
		result += self.z**2
		return result
	def getLength(self):
		return math.sqrt(self.getLengthPow2())
	def nvector(self):
		return vector(-self.x, -self.y, -self.z)
	def __mul__(self, other):
		if isinstance(other, vector):
			return vector(self.x * other.x, self.y * other.y, self.z * other.z)
		elif isinstance(other, (int, float)):
			return vector(self.x * other, self.y * other, self.z * other)
		else:
			NotImplementedError
	def __floordiv__(self, other):
		if isinstance(other, vector):
			return vector(self.x//other.x, self.y//other.y, self.z//other.z)
		elif isinstance(other, (int, float)):
			if (other == 0):
				ZeroDivisionError
			else:
				return vector(self.x//other, self.y//other, self.z//other)

		else:
			NotImplementedError
	def __truediv__(self, other):
		if isinstance(other, vector):
			return vector(self.x/other.x, self.y/other.y, self.z/other.z)
		elif isinstance(other, (int, float)):
			if (other == 0):
				ZeroDivisionError
			else:
				return vector(self.x/other, self.y/other, self.z/other)
		else:
			NotImplementedError
	def __add__(self, other):
		return vector(self.x + other.x, self.y + other.y, self.z + other.z)
	def __sub__(self, other):
		return vector(self.x - other.x, self.y - other.y, self.z - other.z)
#tbh niepotrzebne, += działa sam z siebie
	def add(self, vec):
		self.x += vec.x
		self.y += vec.y
		self.z += vec.z
	def sub(self, vec):
		self.x -= vec.x
		self.y -= vec.y
		self.z -= vec.z	
	def mul(self, vec):
		self.x *= vec.x
		self.y *= vec.y
		self.z *= vec.z
	def div(self, vec):
		self.x /= vec.x
		self.y /= vec.y
		self.z /= vec.z
#te już znowu potrzebne
	def scalar(self, vect):
		return ((self.x * vect.x) + (self.y * vect.y) + (self.z * vect.z))
	def cross(self, vect):
		return vector(self.y*vect.z - self.z*vect.y, self.z*vect.x - self.x*vect.z,self.x*vect.y - self.y * vect.x)
	def normalize(self):
		if (self.getLength() != 0):
			vect = vector(self.x,self.y,self.z)
			vect.x /= self.getLength()
			vect.y /= self.getLength()
			vect.z /= self.getLength()
			return vect
	def __str__(self):
		return ("({},{},{})".format(self.x, self.y, self.z))
	__rmul__ = __mul__
	__radd__ = __add__	
	
	
vec = vector(1, 1, 0)
vec2 = vector(1,1,1)
print(vec.getLength())
print(vec.getLengthPow2())
print(vec.nvector())
print(vec * 2)
print(2 * vec)
print(vec//2)
print(vec/2)
vec.add(vec)
print(vec)
vec.sub(vec/2)
print(vec)
vec += vec
print(vec)
print(vec.scalar(vec2))
print(vec.cross(vec2))
print(vec.normalize())
