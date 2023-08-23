import fnv
import fnv.file
import fnv.reduce
import cv2 as cv
import numpy as np

video_path = "C:\\Users\\U361220\\Desktop\\SEQ Conversion\\Videos\\TermovisionDamage3.seq"
output_folder = "C:\\Users\\U361220\\Desktop\\SEQ Conversion\\SDK Output\\Yazan"
im = fnv.file.ImagerFile(video_path) 