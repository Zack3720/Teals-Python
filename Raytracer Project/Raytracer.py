import json
import math
import png
import os

clear = lambda: os.system('cls')
sceneDict = None
sceneObjects = []
sceneLights = []
clear()
with open('Teals-Python\Raytracer Project\scene.json') as f:
    sceneDict = json.load(f)


class Vector():
    x = None
    y = None
    z = None

    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vector((self.x+other.x),(self.y+other.y),(self.z+other.z))

    def __sub__(self, other):
        return Vector((self.x-other.x),(self.y-other.y),(self.z-other.z))
    
    def __mul__(self, other):
        if type(other) == int or type(other) == float:
            return Vector((self.x*other),(self.y*other),(self.z*other))
        elif type(other) == Vector:
            return Vector((self.x*other.x),(self.y*other.y),(self.z*other.z))
        else:
            raise TypeError('Unsupported operand type for vector')

    def __truediv__(self, other):
        return Vector((self.x/other.x),(self.y/other.y),(self.z/other.z))
    
    def __str__(self):
        return str(self.x) + ' ' + str(self.y) + ' ' + str(self.z)

    @staticmethod
    def dotProduct(v1,v2):
        v3 = v1*v2
        return v3.x+v3.y+v3.z

    def length(self, other = None):
        if other is None:
            other = Vector(0,0,0)
        vsum = self + other
        return math.sqrt(Vector.dotProduct(vsum,vsum))

    def normalize(self, other = None):
        if other is None:
            magnitude = self.length()
        else:
            magnitude = self.length(other)
        self.x /= magnitude
        self.y /= magnitude
        self.z /= magnitude

class Sphere():
    
    def __init__(self, center: Vector, radius: int, color: Vector):

        self.center = center
        self.radius = radius
        self.color = color

class Plane():

    def __init__(self):
        pass

class Ray():

    def __init__(self, direction: Vector, point = None):
        if point is None:
            direction.normalize()
            point = Vector(0,0,0)
        else:
            direction.normalize(point)
        
        self.direction = direction
        self.endpoint = point

    def intersects(self,s: Sphere):
        a = (Vector.dotProduct(self.direction,(self.endpoint-s.center))**2)-(Vector.dotProduct((self.endpoint-s.center),(self.endpoint-s.center))-(s.radius**2))
        if a < 0:
            return Vector(0,0,-1)
        a = math.sqrt(a)
        b = -(Vector.dotProduct(self.direction,(self.endpoint-s.center)))

        if b-a > 0:
            return self.direction*(b-a) + self.endpoint
        elif b+a > 0:
            return self.direction*(b+a) + self.endpoint
        else:
            return Vector(0,0,-1)

def loadScene():
    global sceneDict
    global sceneObjects
    global sceneLights
    for x in sceneDict['shapes']:
        if x['type'] == 'sphere':
            sceneObjects.append(Sphere(Vector(x['transform']['translate']['x'],x['transform']['translate']['y'],x['transform']['translate']['z']),x['radius'],Vector(x['material']['color']['red'],x['material']['color']['green'],x['material']['color']['blue'])))
        else:
            # Append plane here
            pass
    for x in sceneDict['lights']:
        sceneLights.append({'position' : Vector(x['transform']['translate']['x'],x['transform']['translate']['y'],x['transform']['translate']['z']), 'color' : Vector(x['material']['color']['red'],x['material']['color']['green'],x['material']['color']['blue']), 'intensity' : x['intensity']})

def drawImage(fov: int): 
    global sceneDict
    global sceneObjects
    width = sceneDict['output']['width']
    height = sceneDict['output']['height']
    p = []
    v = int((width/2)/math.tan((fov*math.pi/180)/2))

    for i in range(height):
        temp = []
        for j in range(width):
            r = Ray(Vector(int(j-(width/2)),int((height/2))-i,v))
            closestIntersect = -1
            objectIndex = 0

            for x in range(len(sceneObjects)):
                intersect = r.intersects(sceneObjects[x])
                if (intersect.length() < closestIntersect or closestIntersect == -1) and intersect.z != -1:
                    closestIntersect = intersect.length()
                    objectIndex = x
            if closestIntersect == -1:
                temp.extend([int(sceneDict['world']['color']['red']*255),int(sceneDict['world']['color']['green']*255),int(sceneDict['world']['color']['blue']*255)])
            else:
    
                color = sceneObjects[objectIndex].color
                temp.append(int(color.x*255))
                temp.append(int(color.y*255))
                temp.append(int(color.z*255))
        p.append(temp)
    f = open('output.png', 'wb')
    w = png.Writer(width, height, greyscale=False)
    w.write(f, p)
    f.close()
    print('done!')

loadScene()
drawImage(45)
            


