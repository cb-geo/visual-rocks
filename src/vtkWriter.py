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


## MODIFY THIS: TREAT AS IF INPUT FILE JUST HAS LIST FOR EACH OF THESE AS PART OF THE DICTIONARY

# Find number faces for all blocks
ncells = 0
for i in range(0, len(data.blocks)):
    ncells = ncells + len(data.blocks[i])

# Generate list of normal vectors
normals = ()
for i in range(0, len(data.blocks)):
    for j in range()

# Initialize vtk file
vtkBlocks = VtkFile("./blocks", VtkPolyData)
vtkBlocks.openPiece(start = None, end = None,
                    npoints = len(data.vertices), ncells, nverts = len(data.vertices),
                    nlines = None, nstrips = None, npolys = len(data.blocks))


