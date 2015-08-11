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

with open(inputFile, 'r') as f:
    data = json.load(f, object_hook = JSONObject)

# Initialize vtk file
vtkBlocks = VtkFile("./blocks", VtkPolyData)

for i in range(0, len(data) - 1): 
    # Extract data for vtk file creation
    npoints = len(data(i).vertices)
    pointIDs = data(i).vertexIDs
    vertices = data(i).vertices
    npolys = data(i).faceCount
    normals = data(i).normals
    connectivity = data(i).connectivity
    offsets = data(i).offsets
    
    vtkBlocks.openPiece(start = None, end = None,
                        npoints, ncells = None, nverts = None,
                        nlines = None, nstrips = None, npolys)
    
    # Point data
    vtkBlocks.openElement("Points")
    vtkBlocks.addData("Coordinates", vertices)
    vtkBlocks.closeData("Points")
    vtkBlocks.openData("Point", scalars = "pointIDs")
    vtkBlocks.addData("pointIDs", pointIDs)
    vtkBlocks.closeData("Point")

    # Cell data
    vtkBlocks.openData("Cell", normals = "normals")
    vtkBlocks.addData("normals", normals)
    vtkBlocks.closeData("Cell")
    
    # Poly data
    vtkBlocks.openElement("Polys")
    vtkBlocks.addData("connectivity", connectivity)
    vtkBlocks.addData("offsets", offsets)
    vtkBlocks.closeData("Polys")

    # Append data
    vtkBlocks.appendData(vertices)
    vtkBlocks.appendData(pointIDs)
    vtkBlocks.appendData(normals)
    vtkBlocks.appendData(connectivity).appendData(offsets)

vtkBlocks.save()
