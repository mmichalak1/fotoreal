from colour import *
from rendertypes import *
from cameras import *
from objloader import *

from PIL import Image

import multiprocess as mp
from timeit import default_timer as timer

IMAGEWIDTH  = 400
IMAGEHEIGTH = 400

ASPECTRATIO = IMAGEWIDTH / IMAGEHEIGTH

ORTOSIZEX = 100
ORTOSIZEY = ORTOSIZEX / ASPECTRATIO

XSTEP = ORTOSIZEX / IMAGEWIDTH
YSTEP = ORTOSIZEY / IMAGEHEIGTH

oliveMat = material(Color("olive"), 10.0, 50.0, 0.0)
magentaMat = material(Color("Magenta"), 20.0, 0.0, 0.2)
blueMat = material(Color("Blue"), 50.0, 5.0, 1.0)
greenMat = material(Color("Green"), 0.0, 0.0, 0.1)

objects = []

al = Color("lightyellow")
prs = parser()
prs.load_obj("cube.obj")
t = triangle(vector(-50, -20, 50), vector(100, 110, 50), vector(130, 0, 50), magentaMat)

lights = []
lights.append(pointLight(vector(0,0,500), Color("pink"), 1.0, 2.0, 3.0))
objects.append(t)
objects.append(mesh(prs.triangles))
#for tr in prs.triangles:
#	objects.append(tr)
sc = scene(objects, al, lights)
	


cam = perspectiveCam(vector(-30,120,-100), vector(0,-1,10).normalize(), vector(0,10,1).normalize(),10000, 10, 60, ORTOSIZEX, ORTOSIZEY, XSTEP, YSTEP)

def numColToFloat(color):
	return tuple(x/256. for x in color.rgb)
def divColor(col, div):
	return Color(rgb=(col.red/div,col.green/div,col.blue/div))
def floatColToNum(color):
	return tuple(int(x * 256) for x in color.rgb)

def AntyAliasing(camera,x,y,depth,iter=0):
	step = 1/((iter+1)*2)
	cent = camera.parsePixel((x, y), sc)
	LU = camera.parsePixel((x-step, y+step), sc)
	LD = camera.parsePixel((x-step, y-step), sc)
	RU = camera.parsePixel((x+step, y+step), sc)
	RD = camera.parsePixel((x+step, y-step), sc)
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
			pix[x,y] = floatColToNum(AntyAliasing(cam,x + xoffset,y + yoffset,0))
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
	#start = timer()
	#render()
	#end = timer()
	#print("Single process: {}".format(end - start))
	
	start = timer()
	newrender()
	end = timer()
	print("Multi process: {}".format(end - start))


if __name__ == "__main__":
	main()
	




