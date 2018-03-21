from colour import Color
from rendertypes import *
from cameras import *
import threading


from PIL import Image

IMAGEWIDTH  = 800
IMAGEHEIGTH = 600

ASPECTRATIO = IMAGEWIDTH / IMAGEHEIGTH

ORTOSIZEX = 800
ORTOSIZEY = ORTOSIZEX / ASPECTRATIO

XSTEP = ORTOSIZEX / IMAGEWIDTH
YSTEP = ORTOSIZEY / IMAGEHEIGTH

# print(XSTEP, YSTEP)

class pixelThread (threading.Thread):
	def __init__(self, X,Y,depth,camera):
		threading.Thread.__init__(self)
		self.X = X
		self.Y = Y
		self.depth = depth
		self.camera = camera
	def run(self):
		floatColToNum(AntyAliasing(self.camera,self.x,self.y,1))


# print(basicOrig)
threadLock = threading.Lock()
objects = []
objects.append(sphere(vector(0,0,100), 50, Color("Red")))
objects.append(sphere(vector(20, 20, 20), 30, Color("Green")))
def numColToFloat(color):
	return tuple(x/256. for x in color.rgb)
def divColor(col, div):
	return Color(rgb=(col.red/div,col.green/div,col.blue/div))
def addColor(colors):
	col = Color(rgb=(0,0,0))
	for color in colors:
		col.red += color.red
		col.green += color.green
		col.blue += color.blue
	return col
def floatColToNum(color):
	return tuple(int(x*256) for x in color.rgb)

def AntyAliasing(camera,x,y,depth,iter=0):
	step = 1/((iter+1)*2)
	cent = camera.parsePixel((x, y), objects)
	LU = camera.parsePixel((x-step, y+step), objects)
	LD = camera.parsePixel((x-step, y-step), objects)
	RU = camera.parsePixel((x+step, y+step), objects)
	RD = camera.parsePixel((x+step, y-step), objects)
	if (iter < depth):
		if(cent != LU):
			LU = AntyAliasing(x-(step/2),y+(step/2),depth,(iter+1))
		if(cent != LD):
			LU = AntyAliasing(x-(step/2),y-(step/2),depth,(iter+1))
		if(cent != RU):
			LU = AntyAliasing(x+(step/2),y+(step/2),depth,(iter+1))
		if(cent != RD):
			LU = AntyAliasing(x+(step/2),y-(step/2),depth,(iter+1))	
	return addColor((divColor(LU,4),divColor(LD,4),divColor(RU,4),divColor(RD,4)))
	
	
	
def render(objects, camera):
	img = Image.new('RGB', (IMAGEWIDTH, IMAGEHEIGTH), 'black')
	pix = img.load()
	#print("HELLO")
	for x in range(0, IMAGEWIDTH):
		for y in range(0, IMAGEHEIGTH):
			# print("render")
		#	Tempcol = divColor(camera.parsePixel((x, y), objects),5)
		#	Tempcol = addColor((Tempcol,divColor(camera.parsePixel(((x-0.5), (y+0.5)), objects),5)))
		#	Tempcol = addColor((Tempcol,divColor(camera.parsePixel(((x-0.5), (y-0.5)), objects),5)))
		#	Tempcol = addColor((Tempcol,divColor(camera.parsePixel(((x+0.5), (y+0.5)), objects),5)))
		#	Tempcol = addColor((Tempcol,divColor(camera.parsePixel(((x+0.5), (y+0.5)), objects),5)))
		#	pix[x, y] += floatColToNumAA(camera.parsePixel((x-0.5, y-0.5), objects))
		#	pix[x, y] += floatColToNumAA(camera.parsePixel((x+0.5, y+0.5), objects))
		#	pix[x, y] += floatColToNumAA(camera.parsePixel((x+0.5, y-0.5), objects))
		
		#	pix[x,y] += floatColToNum(AntyAliasing(self.camera,self.x,self.y,1))
			pix[x,y] = pixelThread(x,y,1,camera)			
			
	img.show()

cam = ortocam(vector(), vector(0,0,1), 10000,ORTOSIZEX, ORTOSIZEY, XSTEP, YSTEP)
	
render(objects, cam)