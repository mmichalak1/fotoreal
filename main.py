import math


class vector:
	def __init__(self, a, b, c):
		self.a = a
		self.b = b
		self.c = c
	def getLengthPow2(self):
		result = 0
		result += self.a**2 
		result += self.b**2
		result += self.c**2
		return result
	def getLength(self):
		return math.sqrt(self.getLengthPow2())
	def nvector(self):
		return vector(-self.a, -self.b, -self.c)
	def __mul__(self, other):
		if isinstance(other, vector):
			return vector(self.a * other.a, self.b * other.b, self.c * other.c)
		elif isinstance(other, (int, float)):
			return vector(self.a * other, self.b * other, self.c * other)
		else:
			NotImplementedError
	def __floordiv__(self, other):
		if isinstance(other, vector):
			return vector(self.a//other.a, self.b//other.b, self.c//other.c)
		elif isinstance(other, (int, float)):
			if (other == 0):
				ZeroDivisionError
			else:
				return vector(self.a//other, self.b//other, self.c//other)

		else:
			NotImplementedError
	def __truediv__(self, other):
		if isinstance(other, vector):
			return vector(self.a/other.a, self.b/other.b, self.c/other.c)
		elif isinstance(other, (int, float)):
			if (other == 0):
				ZeroDivisionError
			else:
				return vector(self.a/other, self.b/other, self.c/other)
		else:
			NotImplementedError
	def __add__(self, other):
		return vector(self.a + other.a, self.b + other.b, self.c + other.c)
	def __sub__(self, other):
		return vector(self.a - other.a, self.b - other.b, self.c - other.c)
#tbh niepotrzebne, += działa sam z siebie
	def add(self, vec):
		self.a += vec.a
		self.b += vec.b
		self.c += vec.c
	def sub(self, vec):
		self.a -= vec.a
		self.b -= vec.b
		self.c -= vec.c	
	def mul(self, vec):
		self.a *= vec.a
		self.b *= vec.b
		self.c *= vec.c
	def div(self, vec):
		self.a /= vec.a
		self.b /= vec.b
		self.c /= vec.c
	def __str__(self):
		return ("({},{},{})".format(self.a, self.b, self.c))
	__rmul__ = __mul__
	__radd__ = __add__	
	
	
vec = vector(3, 3, 0)

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
