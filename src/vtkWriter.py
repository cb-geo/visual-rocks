#!/usr/bin/python
from pyevtk.vtk import VtkFile, VtkPolyData
import sys
import numpy as np
import json
from pprint import pprint

# This script reads in JSON objects from the specified input file and
# writes them to a xml polygon vtk file.

# First command line argument: Input File (List of coordinates for all vertices,
#                                          block data: normals and connectivity for all faces)

# Defines function to read in JSON objects from input file
class JSONObject:
    def __init__(self, d):
        self.__dict__ = d

# Process command line arguments:
if len(sys.argv) != 2:
    print "Usage: {} <inputFile>".format(sys.argv[0])
    sys.exit(1)
inputFile = str(sys.argv[1])

data = []

with open (inputFile, 'r') as f:
    for line in f:
        data.append(json.loads(line, object_hook = JSONObject))

# Initialize vtk file and open polygon data
vtkBlocks = VtkFile("./blocks", VtkPolyData)
vtkBlocks.openElement("PolyData")

for i in range(0, len(data)):
    # Extract data for vtk file creation
    npoints = len(data[i].vertexIDs)
    pointIDs = np.asarray(data[i].vertexIDs)
    vertices = np.asarray(data[i].vertices)
    npolys = np.asarray(data[i].faceCount)
    normals = np.asarray(data[i].normals)
    connectivity = np.asarray(data[i].connectivity)
    offsets = np.asarray(data[i].offsets)

    vtkBlocks.openPiece(start = None, end = None,
                        npoints = npoints, ncells = None, nverts = None,
                        nlines = None, nstrips = None, npolys = npolys)

    # Point data
    vtkBlocks.openElement("Points")
    vtkBlocks.addHeader("points", vertices.dtype.name, len(pointIDs), 3)
    vtkBlocks.closeElement("Points")
    vtkBlocks.openData("Point", scalars = "pointIDs")
    # vtkBlocks.addData("pointIDs", pointIDs)
    vtkBlocks.addHeader("pointIDs", pointIDs.dtype.name, len(pointIDs), 1)
    vtkBlocks.closeData("Point")

    # Cell data
    vtkBlocks.openData("Cell",  normals = "normals")
    vtkBlocks.addHeader("normals", normals.dtype.name, npolys, 3)
    vtkBlocks.closeData("Cell")

    # Poly data
    vtkBlocks.openElement("Polys")
    vtkBlocks.addHeader("connectivity", connectivity.dtype.name, len(connectivity), 1)
    vtkBlocks.addHeader("offsets", offsets.dtype.name, len(offsets), 1)
    # vtkBlocks.addData("connectivity", connectivity)
    # vtkBlocks.addData("offsets", offsets)
    vtkBlocks.closeElement("Polys")

    vtkBlocks.closePiece()

# Close polygon data
vtkBlocks.closeElement("PolyData")

# Append data for each polygon
for i in range(0, len(data)):
    # Extract data for each piece
    pointIDs = np.asarray(data[i].vertexIDs)
    vertices = np.asarray(data[i].vertices)
    normals = np.asarray(data[i].normals)
    connectivity = np.asarray(data[i].connectivity)
    offsets = np.asarray(data[i].offsets)

    # Append data
    vtkBlocks.appendData(vertices)
    vtkBlocks.appendData(pointIDs)
    vtkBlocks.appendData(normals)
    vtkBlocks.appendData(connectivity)
    vtkBlocks.appendData(offsets)

# Save vtk file
vtkBlocks.save()
