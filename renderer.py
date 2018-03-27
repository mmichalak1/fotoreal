from colour import Color
from rendertypes import *
from cameras import *

from PIL import Image

IMAGEWIDTH  = 800
IMAGEHEIGTH = 600

ASPECTRATIO = IMAGEWIDTH / IMAGEHEIGTH

ORTOSIZEX = 1366
ORTOSIZEY = ORTOSIZEX / ASPECTRATIO

XSTEP = ORTOSIZEX / IMAGEWIDTH
YSTEP = ORTOSIZEY / IMAGEHEIGTH

# print(XSTEP, YSTEP)

# print(basicOrig)
al = Color("lightyellow")
objects = []
objects.append(sphere(vector(0,0,600), 50, Color("Red")))
objects.append(sphere(vector(20, 20, 580), 30, Color("Green")))
# objects.append(sphere(vector())
objects.append(plane(vector(0,-29,800), vector(0,1,0).normalize(), Color("Blue")))

def numColToFloat(color):
	return tuple(x/256. for x in color.rgb)
def divColor(col, div):
	return Color(rgb=(col.red/div,col.green/div,col.blue/div))
def floatColToNum(color):
	return tuple(int(x*256) for x in color.rgb)

def AntyAliasing(camera,x,y,depth,iter=0):
	step = 1/((iter+1)*2)
	cent = camera.parsePixel((x, y), objects)
	return cent
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
	for x in range(0, IMAGEWIDTH):
		for y in range(0, IMAGEHEIGTH):
			pix[x,y] = floatColToNum(AntyAliasing(camera,x,y,0))
			
	img.show()
	# img.save("Hello.bmp")

#cam = ortocam(vector(), vector(0,0,1), vector(0, 1, 0), 10000, ORTOSIZEX, ORTOSIZEY, XSTEP, YSTEP, al)
cam = perspectiveCam(vector(), vector(0,0,1), vector(0,1,0),10000, 10, 90, ORTOSIZEX, ORTOSIZEY, XSTEP, YSTEP, al)

render(objects, cam)