#!/usr/bin/python
from evtk.vtk import VtkFile, VtkPolyData
import sys
import numpy as np
import json
from pprint import pprint

# This script reads in JSON objects from the specified input file and 
# writes them to a xml polygon vtk file. 

# First command line argument: Input file name 

# Defines function to read in JSON objects from input file
class JSONObject:
    def __init__(self, d):
        self.__dict__ = d

# Process command line arguments:
inputFile = str(sys.argv[1])

with open(inputFile, 'r') as f:
    data = json.load(f, object_hook = JSONObject)

