import os

import cv2 as cv
import numpy as np

video = "damage1"
image_format = ".tiff"  # .tiff

COLORMAP = cv.COLORMAP_JET
ROOT_DIR = os.path.dirname(os.getcwd())
IMAGE_DIR = os.path.join(
    ROOT_DIR,
    "Output",
    "split_seqs",
    video,
    "preview" if image_format == ".jpg" else "radiometric",
)
OUTPUT_DIR = os.path.join(ROOT_DIR, "Output", "colormapping", image_format[1:], video)

print(
    """
    -------------------------
    Root directory: {}
    Image directory: {}
    Output directory: {}
    Colormap: {}
    Image format: {}
    Video: {}
    -------------------------
    """.format(
        ROOT_DIR, IMAGE_DIR, OUTPUT_DIR, COLORMAP, image_format, video
    )
)


def make_colour_image(image):
    colored_image = None

    try:
        image = image.astype(float)
        image_min = image.min()
        image_max = image.max()
        image_range = image_max - image_min
        image_scaled = (((image - image_min) / image_range) * 255).astype(np.uint8)
        colored_image = cv.applyColorMap(image_scaled, COLORMAP)
    except RuntimeWarning as e:
        print(f"Error occurred during color image creation: {str(e)}")
        colored_image = None

    return colored_image


def get_images():
    image_list = []
    # Read in images from IMAGE_DIR
    for filename in os.listdir(IMAGE_DIR):
        if filename.endswith(image_format):
            image_path = os.path.join(IMAGE_DIR, filename)
            image = cv.imread(image_path)
            if image is not None:
                image_list.append(image)
    # Return them as a list
    return image_list


if __name__ == "__main__":
    images = get_images()
    for i, image in enumerate(images):
        # Make the image coloured
        color_image = make_colour_image(image)
        image_path = os.path.join(OUTPUT_DIR, f"colormapped_image_{i}.jpg")
        # Save the image
        cv.imwrite(image_path, color_image)
