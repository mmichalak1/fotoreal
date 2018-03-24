from colour import Color
from rendertypes import *
from cameras import *


from PIL import Image

IMAGEWIDTH  = 800
IMAGEHEIGTH = 600

ASPECTRATIO = IMAGEWIDTH / IMAGEHEIGTH

ORTOSIZEX = 1280
ORTOSIZEY = ORTOSIZEX / ASPECTRATIO

XSTEP = ORTOSIZEX / IMAGEWIDTH
YSTEP = ORTOSIZEY / IMAGEHEIGTH

# print(XSTEP, YSTEP)

# print(basicOrig)
threadLock = threading.Lock()
objects = []
objects.append(sphere(vector(0,0,600), 50, Color("Red")))
objects.append(sphere(vector(20, 20, 580), 30, Color("Green")))
objects.append(plane(vector(-10,-10,0), vector(1,1,0).normalize(), Color("Blue")))

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
			LU = AntyAliasing(camera,x-(step/2),y+(step/2),depth,(iter+1))
		if(cent != LD):
			LD = AntyAliasing(camera,x-(step/2),y-(step/2),depth,(iter+1))
		if(cent != RU):
			RU = AntyAliasing(camera,x+(step/2),y+(step/2),depth,(iter+1))
		if(cent != RD):
			RD = AntyAliasing(camera,x+(step/2),y-(step/2),depth,(iter+1))	
	return addColor((divColor(LU,4),divColor(LD,4),divColor(RU,4),divColor(RD,4)))
	
	
def render(objects, camera):
	img = Image.new('RGB', (IMAGEWIDTH, IMAGEHEIGTH), 'black')
	pix = img.load()
	# img.save("Hello.bmp")
	print("Rendering..",end="", flush=True)
	for x in range(0, IMAGEWIDTH):
		print(".",end="", flush=True)
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
			pix[x,y] = floatColToNum(AntyAliasing(camera,x,y,4))
			
	img.show()
	# img.save("Hello.bmp")

cam = ortocam(vector(), vector(0,0,1), vector(0, 1, 0), 10000, ORTOSIZEX, ORTOSIZEY, XSTEP, YSTEP)
cam = perspectiveCam(vector(600,0,600), vector(-1,0,0), vector(0,1,0),10000, 100, 90, ORTOSIZEX, ORTOSIZEY, XSTEP, YSTEP)

render(objects, cam)