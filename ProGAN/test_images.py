import os
import sys
import glob

import PIL.Image

import numpy as np
import tfutil
import dataset

from PIL import UnidentifiedImageError

def error(msg):
    print('Error: ' + msg)
    exit(1)

image_filenames = []
image_dir =  "/dss/dsshome1/lxc06/ga96tum2/NHI_images/images_"

for i in range(1,13):
    image_d = image_dir + str(i)
    image_filenames.extend(sorted(glob.glob(os.path.join(image_d, '*'))))
print(image_filenames)

if len(image_filenames) == 0:
    error('No input images found')
img = np.asarray(PIL.Image.open(image_filenames[0]))

resolution = img.shape[0]
    #print("img.ndim",img.ndim)
    #print("before channel",img.shape)
channels = img.shape[2] if img.ndim == 3 else 1
    #print("channels X",channels)
if img.shape[1] != resolution:
    error('Input images must have the same width and height')
if resolution != 2 ** int(np.floor(np.log2(resolution))):
    error('Input image resolution must be a power-of-two')
if channels not in [1, 3]:
    error('Input images must be stored as RGB or grayscale')

label_dir = "/dss/dsshome1/lxc06/ga96tum2"
label_file = "NHI_labels.npy"

npy_filename = os.path.join(label_dir, label_file)
if os.path.isfile(npy_filename):
    pathology_dict = np.load(npy_filename,allow_pickle=True)
        #pathology_dict = np.load(npy_filename,allow_pickle=True).item()
        #print("pathology_dict",pathology_dict)
    print('Successfully load the label dictionary from "%s"' % label_dir)
else:
    error('No input labels found in "%s"' % label_dir)

order = np.arange(len(image_filenames))
        #print("order",order)
for idx in range(order.size):
    try:
        #print("idx",idx)
        img = PIL.Image.open(image_filenames[order[idx]])# open the image file
        img.verify()
    except (IOError, SyntaxError) as e:
        print("idx",idx)
        print("e",e)
        print('Bad file:', image_filenames[order[idx]],order[idx]) # print out the names of corrupt files
