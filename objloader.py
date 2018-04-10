from colour import *
from rendertypes import *

greyMat = material(Color("Blue"),0.5, 0.5, 0.5, 80.0)

class parser:
	def __init__(self):
		self.vertexes = []
		self.normals = []
		self.triangles = []
		self.groups = []
	def load_obj(self, filename):
		file = open(filename, "r")
		lines = file.readlines()	
		for line in lines:
			self.parse_line(line)

	def parse_line(self, line):
		if line.startswith('#'):
			return
				
		values = line.split()
		if len(values) < 2:
			return
		line_type = values[0]
		args = values[1:]
		if line_type == "g":
			self.groups.append(args[0])
		if line_type == "v":
			self.vertexes.append(vector(float(args[0]),float(args[1]),float(args[2])))
		if line_type == "vn":
			self.normals.append(vector(float(args[0]),float(args[1]),float(args[2])))
		if line_type == "f":
			if "//" in args[0]:
				vecs = []
				norm = args[0].split("//")[1]
				for arg in args:
					vecs.append(arg.split("//")[0])
				self.triangles.append(triangle(self.vertexes[int(vecs[0])-1],self.vertexes[int(vecs[1])-1],self.vertexes[int(vecs[2])-1],greyMat,self.normals[int(norm)-1] ))
			if "/" not in args[0]:
				self.triangles.append(triangle(self.vertexes[int(args[0])-1],self.vertexes[int(args[1])-1],self.vertexes[int(args[2])-1], greyMat))
		
#prs = parser()
#prs.load_obj("cube.obj")
#print(len(prs.vertexes))
#for tr in prs.triangles:
#	print((tr))