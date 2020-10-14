import json
import png
import os

clear = lambda: os.system('cls')
sceneDict = None
clear()


with open('Raytracer Project\scene.json') as f:
    sceneDict = json.load(f)

p = []
temp = [int(sceneDict['world']['color']['red']*255),int(sceneDict['world']['color']['green']*255),int(sceneDict['world']['color']['blue']*255)] * sceneDict['output']['width']
for x in range(sceneDict['output']['height']):
    p.append(temp)
f = open('output.png', 'wb')
w = png.Writer(sceneDict['output']['width'], sceneDict['output']['height'], greyscale=False)
w.write(f, p)
f.close()
