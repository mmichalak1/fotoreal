from colour import Color
from rendertypes import *

from PIL import Image

IMAGEWIDTH  = 800
IMAGEHEIGTH = 600

PIXELWIDTH  = 2. / IMAGEWIDTH
PIXELHEIGTH = 2. / IMAGEHEIGTH

def numColToFloat(color):
	return tuple(x/256. for x in color)

def floatColToNum(color):
	return tuple(int(x*256) for x in color)

	
def parsePixel(coord):
	return floatColToNum(Color("green").rgb)

def render(objects, camera):
	img = Image.new('RGB', (IMAGEWIDTH, IMAGEHEIGTH), 'black')
	pix = img.load()
	for x in range(0, IMAGEWIDTH):
		for y in range(0, IMAGEHEIGTH):
			pix[x, y] = parsePixel((x,y))
	img.show()

render(None, None)