import numpy as np
import matplotlib.pyplot as plt
# purpose: to show the areas where there may be the most difficulty getting a precise position. 
# #This could be used in the future to augment the "getting there" program(the one that gets there) in the future, but for now it is mostly for me getting an idea for my limitations and 
# just generally get a starting point for things(especially how big the whole thing needs to be).


#BASIC methodology(flawed but made to be quick and get things moving):
#   generate a coordinate space, one corner at the origin and one corner at the +,+ winch
#       This is because the thing is symmetric across the x and y axes. could also just do 1/8th but that seems unnecessarily difficult for minimal performance boost
#   at each coordinate, find the distance to each winch, the "winch lengths"
#   To find the sensitivity at a location, find the difference between each of the 4 adjacent coordinate's winch lengths and the target's.
#   The minimum difference for each winch is that winch's sensitivity at that spot
#   We can interpret this data different ways(averages between winches, minimums, medians, etc)

#BETTER methodology
#   generate coord space
#   generate 4 MORE coord spaces which are offset from the originals by [the distance between points] at a 45 degree angle to the axes
#   check the same things but with the adjacent EIGHT this time
#   means that we get better representation of diagonal sensitivities

#What does the data mean?
#   This 'sensitivity value' basically means "How much would the winch have to be off to have the position be off by X much"

#only operating on 1/4 of the screen bc it's symmetrical
#basically is intended to act as a 'how hard will it be to land here' measure


#generates the coord space we work with
#   length - any number format taken by arange; the outer bound of the coords
#   pts - int;  number of points along an axis(total coordspace number of points will be pts^2)
'''def meshgrid_based(length, pts):
    Ypts = np.linspace(0, length, pts)
    Xpts = np.linspace(0, length, pts)
    X2D,Y2D = np.meshgrid(Ypts,Xpts)
    return np.column_stack((Y2D.ravel(),X2D.ravel()))
'''

#distance along one axis from the origin
#basically if this is 2, then the winches are at (2,2)[adjust for signs]
sideLength = 5

#number of points along an axis
pts = 30

#generate coordinate space
y, x = np.meshgrid(np.linspace(0, sideLength, pts), np.linspace(0, sideLength, pts))
coords = np.stack([x, y], 2)
#find the distances
#will try and streamline later, maybe

# winches go counterclockwise, starting from (+,+) quadrant

#makes the operator arrays for finding the 'leg lengths' of the distances to winches
def makeSubArr(x, y, shape, mag):
    #x : -1 or +1, sign of the x
    #y : -1 or +1, sign of the y
    #shape: shape of the needed array
    #mag : the sidelenght
    xOp, yOp = np.meshgrid(mag*x*np.ones(shape[0]), mag*y*np.ones(shape[1]))
    opArr = np.stack([xOp, yOp], 2)
    return opArr
        
#finding the (x2-x1) and (y2-1)
winch1Diff = np.abs(np.subtract(coords, makeSubArr(1, 1, (pts, pts), sideLength)))
winch2Diff = np.abs(np.subtract(coords, makeSubArr(-1, 1, (pts, pts), sideLength)))
winch3Diff = np.abs(np.subtract(coords, makeSubArr(-1, -1, (pts, pts), sideLength)))
winch4Diff = np.abs(np.subtract(coords, makeSubArr(1, -1, (pts, pts), sideLength)))

#finding the actual distances
w1Dist = np.sqrt(np.power(winch1Diff[:,:, 0], 2) + np.power(winch1Diff[:,:, 1], 2))
w2Dist = np.sqrt(np.power(winch2Diff[:,:, 0], 2) + np.power(winch2Diff[:,:, 1], 2))
w3Dist = np.sqrt(np.power(winch3Diff[:,:, 0], 2) + np.power(winch3Diff[:,:, 1], 2))
w4Dist = np.sqrt(np.power(winch4Diff[:,:, 0], 2) + np.power(winch4Diff[:,:, 1], 2))


#processes the values. made a function for easy messing with
def distProcessing(values):
    return np.nanmin(values, 0)

#subtracts each of the adjacent neighbors, subtracts them, and returns the processed value
def offsetSubtract(arr):
    padded = np.pad(arr, (1, 1), 'empty').astype(arr.dtype)
    #offset vector starts to the down, moves counterclockwise
    off1 = padded[2:, 1:-1]
    off2 = padded[:-2, 1:-1]
    off3 = padded[1:-1, 2:]
    off4 = padded[1:-1, :-2]
    return distProcessing([np.abs(np.subtract(arr, off1)), np.abs(np.subtract(arr, off2)), np.abs(np.subtract(arr, off3)), np.abs(np.subtract(arr, off4))])
test1 = offsetSubtract(w1Dist)
plt.imshow(test1, cmap='Greys', origin="lower")
plt.show()