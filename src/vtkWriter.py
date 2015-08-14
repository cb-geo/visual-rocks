#!/usr/bin/python
from evtk.vtk import VtkFile, VtkPolyData
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
inputFile = str(sys.argv[1])

data = []

with open (inputFile, 'r') as f:
    for line in f:       
        data.append(json.loads(line, object_hook = JSONObject))

# Initialize vtk file and open polygon data
vtkBlocks = VtkFile("./blocks", VtkPolyData)
vtkBlocks.openElement("PolyData")

print len(data)

for i in range(0, len(data)): 
    # Extract data for vtk file creation
    npoints = len(data[i].vertexIDs)
    pointIDs = np.asarray(data[i].vertexIDs)
    vertices = np.asarray(data[i].vertices)
    npolys = np.asarray(data[i].faceCount)
    normals = np.asarray(data[i].normals)
    connectivity = np.asarray(data[i].connectivity)
    offsets = np.asarray(data[i].offsets)
    cellIDs = np.arange(0, npolys)
    print "Vertices: " 
    print vertices
    print "Connectivity: " 
    print connectivity
    print "Offsets: " 
    print offsets
    print "Normals:"
    print normals
    
    vtkBlocks.openPiece(start = None, end = None,
                        npoints = npoints, ncells = None, nverts = None,
                        nlines = None, nstrips = None, npolys = npolys)
    
    # Point data
    vtkBlocks.openElement("Points")
    vtkBlocks.addHeader("points", vertices.dtype.name, len(pointIDs), 3)
    vtkBlocks.closeElement("Points")
    # vtkBlocks.openElement("Points")
    # vtkBlocks.addData("points", vertices)
    # vtkBlocks.closeElement("Points")
    vtkBlocks.openData("Point", scalars = "pointIDs")
    vtkBlocks.addData("pointIDs", pointIDs)
    vtkBlocks.closeData("Point")

    # Cell data
    vtkBlocks.openData("Cell", scalars = "cellIDs", normals = "normals")
    vtkBlocks.addHeader("cellIDs", cellIDs.dtype.name, npolys, 1)
    vtkBlocks.addHeader("normals", normals.dtype.name, npolys, 3)
    # vtkBlocks.addData("normals", normals)
    vtkBlocks.closeData("Cell")
    
    # Poly data
    vtkBlocks.openElement("Polys")
    vtkBlocks.addData("connectivity", connectivity)
    vtkBlocks.addData("offsets", offsets)
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
    cellIDs = np.arange(0, npolys)

    # Append data
    vtkBlocks.appendData(vertices)
    vtkBlocks.appendData(pointIDs)
    vtkBlocks.appendData(cellIDs)
    vtkBlocks.appendData(normals)
    vtkBlocks.appendData(connectivity).appendData(offsets)

# Save vtk file
vtkBlocks.save()
