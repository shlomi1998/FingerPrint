#!/usr/bin/env python

"""
This file defines the database of fingerprints images.

Author: Ayelet Zadock
Last modified: 28-05-2018

"""

# Imports:
import os
import glob
import cv2
import pandas as pd
#import tkinter.filedialog as tk # or
#import tkinter.filedialog as tk # or
from tkinter import filedialog
import ntpath
import globalFunctions as gf

filename = filedialog.askopenfilename()
fingerprint = gf.getInputImage(filename)
fingerdata = gf.extractFingerDataFromFilename(fingerprint[-1])

# Standard of filename: <person name: any letter and/or number><hand letter: R/L><finger number: 1/2/3/4/5>
database = {}
DBpath = gf.DBpath
for filename in glob.glob(os.path.join(DBpath, '*.tif')):
    img = cv2.imread(filename)
    [imgName, imgDir, imgPath, imgPrefix] = gf.getInputImage(filename)
    [person, hand, finger, inStandard] = gf.extractFingerDataFromFilename(imgPrefix)

    if inStandard is False:
        print("Filename does not match standard.")
    else:
        hand = {hand+finger: img}
        if person in database.keys():
            prevCountData = database[person]
            hand.update(prevCountData)
        database[person] = hand


df = pd.DataFrame.from_dict(database, orient='index')
print(df)

writer = pd.ExcelWriter(gf.excelDB)
df.to_excel(writer, gf.DBsheet)
writer.save()

print(database)
