from colour import *
from rendertypes import *
from cameras import *

import numpy as np
from PIL import Image

import multiprocess as mp
from timeit import default_timer as timer

IMAGEWIDTH  = 1980
IMAGEHEIGTH = 1080

ASPECTRATIO = IMAGEWIDTH / IMAGEHEIGTH

ORTOSIZEX = 1366
ORTOSIZEY = ORTOSIZEX / ASPECTRATIO

XSTEP = ORTOSIZEX / IMAGEWIDTH
YSTEP = ORTOSIZEY / IMAGEHEIGTH

al = Color("lightyellow")
objects = []
objects.append(sphere(vector(0,0,600), 50, Color("Red")))
objects.append(sphere(vector(20, 20, 580), 30, Color("Green")))
objects.append(plane(vector(0,-29,800), vector(0,1,0).normalize(), Color("Blue")))

# cam = ortocam(vector(), vector(0,0,1), vector(0, 1, 0), 10000, ORTOSIZEX, ORTOSIZEY, XSTEP, YSTEP, al)
cam = perspectiveCam(vector(), vector(0,0,1), vector(0,1,0),10000, 10, 90, ORTOSIZEX, ORTOSIZEY, XSTEP, YSTEP, al)

def numColToFloat(color):
	return tuple(x/256. for x in color.rgb)
def divColor(col, div):
	return Color(rgb=(col.red/div,col.green/div,col.blue/div))
def floatColToNum(color):
	return tuple(int(x * 256) for x in color.rgb)

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
		
def render():
	img = Image.new('RGB', (IMAGEWIDTH, IMAGEHEIGTH), 'black')
	pix = img.load()
	for x in range(0, IMAGEWIDTH):
		for y in range(0, IMAGEHEIGTH):
			pix[x,y] = floatColToNum(AntyAliasing(cam,x,y,0))
			
	img.show()

def renderJob(width, heigth, xoffset, yoffset, d, id):
	img = Image.new('RGB', (width, heigth), 'black')
	pix = img.load()
	for x in range(width):
		for y in range(heigth):
			pix[x,y] = floatColToNum(AntyAliasing(cam,x + xoffset,y + yoffset,10))
	d[id]=img

def bind(d, hh, hw):
	img =  Image.new('RGB', (IMAGEWIDTH, IMAGEHEIGTH))
	img.paste(d[0], (0,0))
	img.paste(d[1], (0,hh))
	img.paste(d[2], (hw,0))
	img.paste(d[3], (hw,hh))
	return img
	
def newrender():
	hwidth = int(IMAGEWIDTH/2)
	hheigth = int(IMAGEHEIGTH/2)
	procs = []
	man = mp.Manager()
	d = man.dict()
	id = 0
	for i in range(0,2):
		for j in range(0,2):
			p = mp.Process(target=renderJob, args=(hwidth, hheigth, hwidth * i, hheigth * j, d, id))
			id+=1
			p.start()
			procs.append(p)
	for p in procs:
		p.join()
	img = bind(d, hheigth, hwidth)
	img.show()
	
def main():
	start = timer()
	render()
	end = timer()
	print("Single process: {}".format(end - start))
	
	start = timer()
	newrender()
	end = timer()
	print("Multi process: {}".format(end - start))


if __name__ == "__main__":
	main()
	




