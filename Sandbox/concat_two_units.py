# DESCRIPTION
# This code was meant to test whether using a duplicated third channel would result in 
# proper frames being extracted.
#
# RESULTS
# It works, surprisingly. Though the images seem a bit more blurry than usual.
# So I should use three units if possible, but two are okay. One definitely isn't, though.

import os

import cv2
import fnv
import fnv.file
import fnv.reduce
import numpy as np
from tqdm import tqdm
# from pprint import PrettyPrinter
# pprint = PrettyPrinter().pprint

# Define constants
VIDEO_PATH = "C:\\Users\\U361220\\Desktop\\SEQ Conversion\\Videos\\TermovisionDamage3.seq"
OUTPUT_FOLDER = os.path.join(os.getcwd(), 'Frames')
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)
SCALE =  np.uint16
    
# Get readers
im_counts = fnv.file.ImagerFile(VIDEO_PATH)  # reader for COUNTS unit
im_temp = fnv.file.ImagerFile(VIDEO_PATH)  # reader for TEMPERATURE_FACTORY unit
im_signal = fnv.file.ImagerFile(VIDEO_PATH)  # reader for OBJECT_SIGNAL unit

# Extract frames from each
concated_frames = np.empty((im_counts.height, im_counts.width, 3))
for i in tqdm(range(im_counts.num_frames)):
    im_counts.unit = fnv.Unit.COUNTS  # Set the desired unit
    im_counts.get_frame(i)  # Initialize im_counts.final
    im_min = min(im_counts.final)
    im_max = max(im_counts.final)
    im_range = im_max - im_min
    counts_final_unscaled = np.array(im_counts.final, copy=False).reshape((im_counts.height, im_counts.width))  # Reshape frame values
    counts_final = (((counts_final_unscaled - im_min) / im_range) * 255).astype(SCALE)  # Scale for jpeg
    
    # Repeat for temperature unit
    im_temp.unit = fnv.Unit.TEMPERATURE_FACTORY
    im_temp.get_frame(i)
    im_min = min(im_temp.final)
    im_max = max(im_temp.final)
    im_range = im_max - im_min
    temp_final_unscaled = np.array(im_temp.final, copy=False).reshape((im_temp.height, im_temp.width))
    temp_final = (((temp_final_unscaled - im_min) / im_range) * 255).astype(SCALE)

    # # Repeat for radiance unit
    # im_signal.unit = fnv.Unit.OBJECT_SIGNAL
    # im_signal.get_frame(i)
    # im_min = min(im_signal.final)
    # im_max = max(im_signal.final)
    # im_range = im_max - im_min
    # signal_final_unscaled = np.array(im_signal.final, copy=False).reshape((im_signal.height, im_signal.width))
    # signal_final = (((signal_final_unscaled - im_min) / im_range) * 255).astype(SCALE)

    # Reshape into a (480, 640, 3) array for jpg
    concated_frames = np.array([counts_final, temp_final, temp_final]).swapaxes(0, 2).swapaxes(1, 0)
    
    # Save the image
    cv2.imwrite(f'{OUTPUT_FOLDER}\\concat_frame_{i}.jpeg', concated_frames)