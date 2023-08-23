import os
import argparse

import cv2
import fnv
import fnv.file
import numpy as np
from tqdm import tqdm


def make_parser():
    """Make the parser object"""

    parser = argparse.ArgumentParser(
        description="Extracts frames from a seq file into a folder in the current workspace. You can specify multiple files at once. See --help for details.",
    )
    parser.add_argument(
        "filenames",
        help="The names of the .seq files for conversion. To specify multiple files, just write their names one after another.",
        nargs="+",
        type=str,
    )
    parser.add_argument(
        "--output-format",
        help='The file format to save the frames in. Choose between "png" and "jpeg". Defaults to png.',
        choices=["png", "jpeg"],
        required=False,
        default="png",
    )
    parser.add_argument(
        "--output-folder",
        help="The folder to output the extracted frames to. Creates intermediary folders if they do not exist. Defaults to the current directory",
        required=False,
    )
    return parser


def parse(parser):
    """Parse the command line arguments"""

    # Get parsed arguments
    args = parser.parse_args()
    filenames = args.filenames
    output_format = args.output_format if args.output_format else "png"
    output_folder = args.output_folder if args.output_folder else os.getcwd()

    # Save frames in a folder called "Frames"
    output_folder = os.path.join(output_folder, "Frames")

    # Try to create the folder for the extracted frames if it doesn't already exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    return filenames, output_format, output_folder


def open_file(filename):
    # Open the first file and check for errors
    try:
        im_1 = fnv.file.ImagerFile(filename)
    except OSError as e:
        print(f"The file {filename} could not be found.\n\tMake sure you call this program from the same folder as the file, or specify the full path of the file.")
        raise e
    except Exception as e:
        print(f"The file {filename} could not be opened by the ImagerFile module. Try restarting the program.")
        raise e
    
    # Try to open two more for the other units
    try:
        im_2 = fnv.file.ImagerFile(filename)
        im_3 = fnv.file.ImagerFile(filename)
    except Exception as e:
        print(f"The file {filename} could not be opened by the ImagerFile module. Try restarting the program.")
        raise e

    return im_1, im_2, im_3
    

def extract(filenames, output_format, output_folder):
    """Extract the frames """

    # Repeat for each requested .seq file
    for filename in tqdm(filenames):
        # Open .seq file for reading
        im_1, im_2, im_3 = open_file(filename)

        # Set frame units
        allowed_units_list = list(im_1.supported_units)
        check_length(allowed_units_list)
        im_1.unit = allowed_units_list[0]
        im_2.unit = allowed_units_list[1]
        im_3.unit = allowed_units_list[2]

        # Extract and save frames
        for i in tqdm(range(im_1.num_frames)):
            frame_1 = get_scaled_frame(im_1, i)
            frame_2 = get_scaled_frame(im_2, i)
            frame_3 = get_scaled_frame(im_3, i)

            # Concatenate the frames to have three channels
            concated = (
                np.array([frame_1, frame_2, frame_3])
                .swapaxes(0, 2)
                .swapaxes(1, 0)
            )

            # Save the image
            frame_name = f"frame_{i}.{output_format}"
            output_path = os.path.join(output_folder, frame_name)
            result = cv2.imwrite(output_path, concated)
            if result is False:
                print(f"Frame {i} could not be saved.")

        # Close the file readers
        im_1.close()
        im_2.close()
        im_3.close()


def get_scaled_frame(im, frame_i):
    # Initialize im.final
    im.get_frame(frame_i)  

    # Get statistics for normalizing
    im_min = min(im.final)
    im_max = max(im.final)
    im_range = im_max - im_min
    
    # Reshape, normalize, and scale frame values to between 0-255
    frame = np.array(im.final, copy=False).reshape((im.height, im.width))
    frame_scaled = (((frame - im_min) / im_range) * 255).astype(np.uint16)
    
    return frame_scaled


def check_length(supported_units):
    # if len(supported_units) == 0:  # Should never happen
    #     raise Exception(
    #         "There are no thermal units supported for this video. Are you sure it's not corrupted?"
    #     )
    # elif len(supported_units) < 2:
    #     raise Exception(
    #         "This seq files supports less than two units, so it cannot be extracted into RGB frames because that requires three channels."
    #     )
    if len(supported_units) < 3:
        raise Exception("This seq files supports less than three units, so it cannot be extracted into RGB frames because that requires three channels.")


def success():
    """Print a success message."""
    succ = """\
        
        ------------------------------
        
        | Files extracted successfully!
        | Find them in {}
        
        ------------------------------
        """.format(
        output_folder
    )
    print(succ)


if __name__ == "__main__":
    # Create parser
    parser = make_parser()

    # Parse args
    filenames, output_folder, output_path = parse(parser)

    # Extract frames to folder
    extract(filenames, output_folder, output_path)

    # Print success
    success()
