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

class vector():

    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return vector((self.x+other.x),(self.y+other.y),(self.z+other.z))

    def __sub__(self, other):
        return vector((self.x-other.x),(self.y-other.y),(self.z-other.z))
    
    def __mul__(self, other):
        if type(other) == int or type(other) == float:
            return vector((self.x*other),(self.y*other),(self.z*other))
        elif type(other) == vector:
            return vector((self.x*other.x),(self.y*other.y),(self.z*other.z))
        else:
            raise TypeError('Unsupported operand type for vector')

    def __truediv__(self, other):
        return vector((self.x/other.x),(self.y/other.y),(self.z/other.z))
    
    def __str__(self):
        return str(self.x) + ' ' + str(self.y) + ' ' + str(self.z)

    @staticmethod
    def dot(v1,v2):
        v3 = v1*v2
        return v3.x+v3.y+v3.z


v1 = vector(5,6,3)


v2 = vector(7,2,5)
print(v1*2)

