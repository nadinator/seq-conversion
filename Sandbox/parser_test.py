import argparse
import os

parser = argparse.ArgumentParser(
    prog="seq_converter",
    description="Extracts frames from a seq file into a folder in the current workspace.",
    epilog="",
)
parser.add_argument('folder', help='The folder to output the extracted frames to. Defaults to the current directory') 

args = parser.parse_args()
folder = args.folder
new_file = os.path.join(folder, 'newfile.txt')
with open(new_file, 'w+') as f:
    f.write('hi!')
    
# IT WORKS!!!!