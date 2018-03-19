from colour import Color
from rendertypes import *
from cameras import *


from PIL import Image

IMAGEWIDTH  = 800
IMAGEHEIGTH = 600

ASPECTRATIO = IMAGEWIDTH / IMAGEHEIGTH

ORTOSIZEX = 800
ORTOSIZEY = ORTOSIZEX / ASPECTRATIO

XSTEP = ORTOSIZEX / IMAGEWIDTH
YSTEP = ORTOSIZEY / IMAGEHEIGTH

# print(XSTEP, YSTEP)

# print(basicOrig)
objects = []
objects.append(sphere(vector(0,0,100), 50, Color("Red")))
objects.append(sphere(vector(20, 20, 20), 30, Color("Green")))
def numColToFloat(color):
	return tuple(x/256. for x in color.rgb)

def floatColToNum(color):
	return tuple(int(x*256) for x in color.rgb)

def render(objects, camera):
	img = Image.new('RGB', (IMAGEWIDTH, IMAGEHEIGTH), 'black')
	pix = img.load()
	#print("HELLO")
	for x in range(0, IMAGEWIDTH):
		for y in range(0, IMAGEHEIGTH):
			# print("render")
			pix[x, y] = floatColToNum(camera.parsePixel((x, y), objects))
	img.show()

cam = ortocam(vector(), vector(0,0,1), ORTOSIZEX, ORTOSIZEY, XSTEP, YSTEP)
	
render(objects, cam)