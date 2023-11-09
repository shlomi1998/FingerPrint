
# Imports:
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import datetime
from PIL import Image, ImageTk, ImageEnhance, ImageFilter
import numpy as np
import cv2
from matplotlib import pyplot as plt

HEIGHT = 650
WIDTH = 700

HEIGHT2 = 500
WIDTH2 = 500
text_window = "Digital Fingerprint Sweat-Pore Analysis"

past = 3

save_path = "results/"

