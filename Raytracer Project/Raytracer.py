import json
import math
import png
import os

clear = lambda: os.system('cls')
sceneDict = None
sceneObjects = []
sceneLights = []
clear()
with open('Raytracer Project\scene.json') as f:
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
        if not(type(other) == Vector):
            raise TypeError('Unsupported type for vector length')
        vsum = self - other
        return math.sqrt(Vector.dotProduct(vsum,vsum))

    def normalize(self):
        magnitude = self.length()
        x = (self.x)/magnitude
        y = (self.y)/magnitude
        z = (self.z)/magnitude
        return Vector(x,y,z)

class Sphere():
    
    def __init__(self, center: Vector, radius: int, color: Vector, ambient: float, diffuse: float):

        if ambient > 1.0: 
            ambient = 1.0
        if diffuse > 1.0:
            diffuse = 1.0
        self.diffuse = diffuse
        self.ambient = ambient
        self.center = center
        self.radius = radius
        self.color = color

class Plane():

    def __init__(self, position, color: Vector, ambient: float, diffuse: float):
        if ambient > 1.0: 
            ambient = 1.0
        if diffuse > 1.0:
            diffuse = 1.0
        self.center = position
        self.color = color
        self.ambient = ambient
        self.diffuse = diffuse

class Ray():

    def __init__(self, direction: Vector, point = None):
        if point is None:
            normDirection = direction.normalize()
            point = Vector(0,0,0)
        else:
            normDirection = (direction-point).normalize()
        
        self.direction = normDirection
        self.endpoint = point

    def intersects(self,intersecting_object):
        if type(intersecting_object) is Sphere:
            a = (Vector.dotProduct(self.direction * 2,(self.endpoint-intersecting_object.center))**2)-(Vector.dotProduct((self.endpoint-intersecting_object.center),(self.endpoint-intersecting_object.center))-(intersecting_object.radius**2)) * 4
            if a < 0:
                return Vector(0,0,-1)
            a = math.sqrt(a)
            a /= 2
            b = -(Vector.dotProduct(self.direction,(self.endpoint-intersecting_object.center)))

            if b-a > 0:
                return self.direction*(b-a) + self.endpoint
            elif b+a > 0:
                return self.direction*(b+a) + self.endpoint
            else:
                return Vector(0,0,-1)
        elif type(intersecting_object) is Plane:
            if self.direction.y == 0:
                return Vector (0,0,-1)
            
            t_factor = intersecting_object.center.y / self.direction.y
            if t_factor < 0:
                return Vector(0,0,-1)
            return self.direction * t_factor


def loadScene():
    global sceneDict
    global sceneObjects
    global sceneLights
    for x in sceneDict['shapes']:
        position = x['transform']['translate']
        color = x['material']['color']
        if x['type'] == 'sphere':
            sceneObjects.append(Sphere(Vector(position['x'],position['y'],position['z']),x['radius'],Vector(color['red'],color['green'],color['blue']),x['material']['ambient'],x['material']['diffuse']))
        elif x['type'] == 'plane':
            sceneObjects.append(Plane(Vector(position['x'],position['y'],position['z']),Vector(color['red'],color['green'],color['blue']),x['material']['ambient'],x['material']['diffuse']))
    for x in sceneDict['lights']:
        sceneLights.append({'position' : Vector(x['transform']['translate']['x'],x['transform']['translate']['y'],x['transform']['translate']['z']), 'color' : Vector(x['color']['red'],x['color']['green'],x['color']['blue']), 'intensity' : x['intensity']})

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
            intersectPoint = Vector(0,0,0)

            #Finds what(if any) objects that are intersected by ray r
            for x in range(len(sceneObjects)):
                intersect = r.intersects(sceneObjects[x])
                if (intersect.length() < closestIntersect or closestIntersect == -1) and intersect.z > 0:
                    closestIntersect = intersect.length()
                    objectIndex = x
                    intersectPoint = r.direction * intersect.length()
                    
            #Adds color to the list temp
            if closestIntersect == -1:
                temp.extend([int(sceneDict['world']['color']['red']*255),int(sceneDict['world']['color']['green']*255),int(sceneDict['world']['color']['blue']*255)])
            else:
                colors = []
                in_shadow = False
                for x in range(len(sceneLights)):
                    lightRay = Ray(sceneLights[x]['position'],intersectPoint)
                    for y in range(len(sceneObjects)):
                        if y == objectIndex:
                            continue
                        if type(sceneObjects[y]) is Plane:
                            continue
                        light_intersect = lightRay.intersects(sceneObjects[y])
                        if light_intersect.z != -1:
                            in_shadow = True
                    if not(in_shadow):
                        if type(sceneObjects[objectIndex]) is Sphere:
                            objectPoint = lightRay.endpoint-sceneObjects[objectIndex].center
                        elif type(sceneObjects[objectIndex]) is Plane:
                            objectPoint = Vector( 0, -sceneObjects[objectIndex].center.y, 0)
                        objectPoint = objectPoint.normalize()
                        normalFactor = Vector.dotProduct(lightRay.direction,objectPoint)
                        intestFactor = 6
                        #final_color = ambient * shape_color + diffuse * normal_factor * light_color * intensity * shape_color * (1 / distance^2)
                        #colors.append(objectPoint)
                        colors.append(sceneObjects[objectIndex].color * sceneObjects[objectIndex].ambient + (sceneObjects[objectIndex].color * sceneLights[x]['color'] * sceneLights[x]['intensity'] * intestFactor * normalFactor * sceneObjects[objectIndex].diffuse * ( 1 / ((intersectPoint.length(sceneLights[x]['position'])**2) ))))
                    
                color = Vector(0,0,0)
                for x in colors:
                    color = color + x
                color = color * 255
                if color.x > 255:
                    color.x = 255
                elif color.x < 0:
                    color.x = 0
                if color.y > 255:
                    color.y = 255
                elif color.y < 0:
                    color.y = 0
                if color.z > 255:
                    color.z = 255
                elif color.z < 0:
                    color.z = 0
                temp.append(int(color.x))
                temp.append(int(color.y))
                temp.append(int(color.z))
        p.append(temp)
    f = open('output.png', 'wb')
    w = png.Writer(width, height, greyscale=False)
    w.write(f, p)
    f.close()
    print('done!')

loadScene()
drawImage(45)
            


