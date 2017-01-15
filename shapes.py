from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import math
import cv2 as cv
import numpy as np
import random

###
# Puts some shapes on an image to create test data set
###

class Shape():
    points = np.array([])
    midpoint = [0,0] # All shapes should be centered around (0,0)
    width = 0.0
    height = 0.0
    reach = 0.0

    # Takes a list of coordinates and translate them a certain amount
    def translate(self, x, y):
        self.points = np.array([point + [x,y] for point in self.points])
        self.midpoint = self.midpoint + [x,y]
        return self

# Makes an equilateral triangle 
class EquiTriangle(Shape):
    def __init__(self, sideLength):
        self.width = float(sideLength)
        self.height = math.sqrt(math.pow(self.width, 2) + math.pow(self.width/2, 2))
        self.reach = math.ceil(self.height/2)        
        top = [self.height/2, 0]
        left = [-self.height/2, -self.width/2]
        right = [-self.height/2, self.width/2]
        self.points = np.array(np.around([top, left, right]), np.int16)  

class Square(Shape):
    def __init__(self, sideLength):
        self.width = float(sideLength)
        self.height = self.width 
        self.reach = self.width/2.0
        tl = [-self.reach, self.reach]
        tr = [self.reach, self.reach]
        bl = [-self.reach, -self.reach]
        br = [self.reach, -self.reach]
        self.points = np.array(np.around([tl, tr, br, bl]), np.int16)

def distanceBetweenPoints(a, b):
    return math.sqrt(math.pow(a[0] - b[0], 2) + math.pow(a[0] - b[0], 2))

class ImageWithShapes():
    width = 0
    height = 0
    image = np.array([])
    shapes = None
    shapeFill = None

    def __init__(self, width, height, shapes, shapeFill, backgroundFill=0):
        self.image = np.full((width, height), backgroundFill, np.uint8)
        self.width = width
        self.height = height
        self.shapes = shapes
        self.shapeFill = shapeFill
        self.placeShapes()

    # Place the shapes together (without overlapping) (not optimized.. it just works)
    def placeShapes(self, shapes=None):
        shapes = self.shapes if shapes == None else shapes
        midpointsAndReach = []  # [[x, y, reach], ...]

        # Randomly assign midpoints of shapes without overlap
        retries = 5
        for shape in shapes:
            for i in range(retries):  # Max 5 tries        
                # Random placement
                shift = [random.randint(int(shape.width), int(self.width - shape.width)), random.randint(int(shape.height), int(self.height - shape.height))]
                newMidpoint = [shift[0], shift[1]]
                # Check for overlap 
                overlap = False
                for point in midpointsAndReach:
                    if distanceBetweenPoints(newMidpoint, point[:2]) < shape.reach + point[2]:
                        overlap = True
                        break
                if overlap:
                    if i  == retries - 1:
                        print("<> Uh oh, need to replace all shapes")
                        return self.place(image, shapes) # Ran out of tries, start completely over
                    else :    
                        continue # More retries so randomly place shape again
                newMidpoint.append(shape.reach)
                midpointsAndReach.append(newMidpoint)
                break # Next shape
        
        self.setShapes(np.array(midpointsAndReach)[:,:2])
        self.drawShapes()       

    # Assign midpoints to the shapes
    def setShapes(self, midpoints, shapes=None):
        shapes = self.shapes if shapes == None else shapes    

        for i in range(len(shapes)):
            # Find how much to adjust to get to the new midpoint
            x = midpoints[i][0] - shapes[i].midpoint[0]
            y = midpoints[i][1] - shapes[i].midpoint[1]
            shapes[i].translate(x, y)

    # Draw list of shapes onto the image
    def drawShapes(self, fill=None, image=None, shapes=None):
        fill = self.shapeFill if fill == None else fill
        image = self.image if image == None else image
        shapes = self.shapes if shapes == None else shapes 

        for shape in shapes:
            cv.fillConvexPoly(image, np.int32(shape.points), color=fill)

imageSize = 100
triangleWidth = 10.0
squareWidth = 10.0

# Create shapes
triangle = EquiTriangle(triangleWidth)
square = Square(squareWidth)

# Create iamge
image = ImageWithShapes(imageSize, imageSize, [triangle, square], (255, 255, 255))
triangleOnly = np.full((imageSize, imageSize), 255, np.uint8)
image.drawShapes((0,0,0), triangleOnly, [image.shapes[0]])

#Display the image
cv.imshow("image", np.rot90(image.image))
cv.imshow("trianlge", np.rot90(triangleOnly))
cv.waitKey(0)

