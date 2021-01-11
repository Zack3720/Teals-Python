import json
import math
import png
import os

clear = lambda: os.system('cls')
clear()

def parse_vector(dict):
    return Vector(dict['x'], dict['y'], dict['z'])

def parse_color(dict):
    return Vector(dict['red'], dict['green'], dict['blue'])

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


def drawImage(sceneFile):

    sceneDict = None
    sceneObjects = []
    sceneLights = []

    with open(sceneFile) as f:
        sceneDict = json.load(f)
    for shapeDict in sceneDict['shapes']:
        position = shapeDict['transform']['translate']
        color = shapeDict['material']['color']
        if shapeDict['type'] == 'sphere':
            sceneObjects.append(Sphere(
                parse_vector(position),
                shapeDict['radius'],
                parse_color(color),
                shapeDict['material']['ambient'],
                shapeDict['material']['diffuse']))
        elif shapeDict['type'] == 'plane':
            sceneObjects.append(Plane(
                parse_vector(position),
                parse_color(color),
                shapeDict['material']['ambient'],
                shapeDict['material']['diffuse']))
    for lightDict in sceneDict['lights']:
        sceneLights.append({
            'position' : parse_vector(lightDict['transform']['translate']),
            'color' : parse_color(lightDict['color']),
            'intensity' : lightDict['intensity']})

    FOV = sceneDict['camera']['field_of_view']
    width = sceneDict['output']['width']
    height = sceneDict['output']['height']
    pixels = []

    # Finding distance from camera the ray will be at.
    v = int((width/2)/math.tan((FOV*math.pi/180)/2))

    #Loops through every vertical row of the image
    for i in range(height):
        #Stores the imformation for each pixel in a given row
        temp = []
        #Loops through every pixel in current vertical row
        for j in range(width):

            # Constructs ray R using the points (j-w/2,h/2-i,v)
            r = Ray(Vector(int(j-(width/2)),int((height/2))-i,v))

            # Constructs ClosestIntersect and assigns a value of -1, which would be behind the camera.
            closestIntersect = -1

            # Will be the index of the object that was intersected.
            objectIndex = 0

            # Blank vector to be set to point of intersection.
            intersectPoint = Vector(0,0,0)

            #Finds what(if any) objects that are intersected by ray r
            for x in range(len(sceneObjects)):
                #
                intersect = r.intersects(sceneObjects[x])
                if (intersect.length() < closestIntersect or closestIntersect == -1) and intersect.z > 0:
                    closestIntersect = intersect.length()
                    objectIndex = x
                    intersectPoint = r.direction * intersect.length()
                    
            #Adds color to the list temp
            if closestIntersect == -1:
                # If no objects were intersected
                temp.extend([int(sceneDict['world']['color']['red']*255),int(sceneDict['world']['color']['green']*255),int(sceneDict['world']['color']['blue']*255)])
            else:

                # Empty list that will be vectors that correspond to color
                # Each color will be summed up to a final color
                colors = []

                # Boolean if for a specific light, if the point is in a shadow.
                in_shadow = False

                # For loop for every light in the scene
                # In here it will be tested if for each light, a point is in a shadow
                # and if not it will determind one of the colors of the current pixel.
                for x in range(len(sceneLights)):
                    
                    # Constructs ray that starts at intersectPoint from before, 
                    # and goes toward the position of the current light
                    lightRay = Ray(sceneLights[x]['position'],intersectPoint)

                    # For loop for every Object in the scene
                    # In here it will be determind if the pixel is in a shadow for each object.
                    for y in range(len(sceneObjects)):

                        # This will skip this object if it is the object that was intersected with the camera ray.
                        # This is because an object can't cast a shadow onto its self.
                        if y == objectIndex:
                            continue

                        # This will skip the object if it is a Plane
                        # While this also means Planes now can't have shadows
                        # Since in the scene Planes never had a shadow that was visable.
                        # This probably should be changed so that if a new Plane was added it could have a shadow.
                        if type(sceneObjects[y]) is Plane:
                            continue
                        
                        # Constructs light_intersect and sets it to the point at which lightRay
                        # and the current object intersect if they even do.
                        light_intersect = lightRay.intersects(sceneObjects[y])

                        # Test if there was an intersection for this object.
                        if light_intersect.z != -1:
                            
                            # If so makes in_shadow true 
                            in_shadow = True

                            # breaks since there is no point in testing if more objects 
                            # cast a shadow on this point since it won't change anything.
                            break
                    
                    # If the point was not in a shadow, the color will be determinded
                    if not(in_shadow):
                        # Constructs objectPoint for if the point is on a sphere or plane.
                        if type(sceneObjects[objectIndex]) is Sphere:

                            # This vector is pointed in the direction from 
                            # the center of a sphere to point intersected.
                            objectPoint = lightRay.endpoint-sceneObjects[objectIndex].center

                        elif type(sceneObjects[objectIndex]) is Plane:

                            # This vector is pointed in the direction 
                            # opposite of a plane which can only be horizonatal.
                            objectPoint = Vector( 0, -sceneObjects[objectIndex].center.y, 0)

                        # Normalize objectPoint
                        objectPoint = objectPoint.normalize()
                        
                        # Makes the Normal factor by comparing how simular(parellel) the light ray
                        # intersecting the object is to the direction, which way the point was 'facing', of the object
                        normalFactor = Vector.dotProduct(lightRay.direction,objectPoint)

                        # Calculates one of the colors for this point.
                        # Lots of math here, its works so not going to change much about it.
                        colors.append(sceneObjects[objectIndex].color * sceneObjects[objectIndex].ambient + (sceneObjects[objectIndex].color * sceneLights[x]['color'] * sceneLights[x]['intensity'] * normalFactor * sceneObjects[objectIndex].diffuse * ( 1 / ((intersectPoint.length(sceneLights[x]['position'])) ))))
                        # final_color = ambient * shape_color + diffuse * normal_factor * light_color * intensity * shape_color * (1 / distance^2)
                
                color = Vector(0,0,0)
                for x in colors:
                    color = color + x
                color = color * 255
                # Appends the values of the color vector to the temp list
                temp.append(max(0,min(255,int(color.x))))
                temp.append(max(0,min(255,int(color.y))))
                temp.append(max(0,min(255,int(color.z))))
        pixels.append(temp)
    output_file = open('output.png', 'wb')
    w = png.Writer(width, height, greyscale=False)
    w.write(output_file, pixels)
    output_file.close()
    print('done!')

drawImage('Raytracer Project\scene.json')
            


