
# Imports:
import os
import glob
import cv2
import numpy as np
import pandas as pd
# import tkinter.filedialog as tk # or
from tkinter import filedialog
import tkinter as tk
from tkinter import messagebox

import globalFunctions as gf
from globalFunctions import *
# from pyimagesearch.panorama import Stitcher
import argparse
import imutils
from stitch import Stitcher
from PIL import Image, ImageChops

import time
import scipy.misc
import sys

import pymysql
pymysql.install_as_MySQLdb()

ZERO = 0


def OpenFile():
    filename = filedialog.askopenfilename()  # open a dialog to get a path to image file
    if len(filename) == ZERO:
        sys.exit("There is no attached file.\nSystem is exit.")

    return filename


filename = OpenFile()


fpA = oegraphsim.OEFingerPrint()
fpB = oegraphsim.OEFingerPrint()
if not fpA.IsValid():
    print("uninitialized fingerprint")

mol = oechem.OEGraphMol()
oechem.OESmilesToMol(mol, "c1ccccc1")

oegraphsim.OEMakeFP(fpA, mol, oegraphsim.OEFPType_Path)
oegraphsim.OEMakeFP(fpB, mol, oegraphsim.OEFPType_Lingo)

if oegraphsim.OEIsFPType(fpA, oegraphsim.OEFPType_Lingo):
    print("Lingo")
if oegraphsim.OEIsFPType(fpA, oegraphsim.OEFPType_Path):
    print("Path")

if oegraphsim.OEIsSameFPType(fpA, fpB):
    print("same fingerprint types")
else:
    print("different fingerprint types")
