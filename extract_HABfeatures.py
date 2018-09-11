"""
This script generates extracted features for each video, which other
models make use of.

You can change you sequence length and limit to a set number of classes
below.

class_limit is an integer that denotes the first N classes you want to
extract features from. This is useful is you don't want to wait to
extract all 101 classes. For instance, set class_limit = 8 to just
extract features for the first 8 (alphabetical) classes in the dataset.
Then set the same number when training models.
"""
import glob
import numpy as np
import os.path
from dataHAB import DataSet
from extractor import Extractor
from tqdm import tqdm
#import pdb; pdb.set_trace()
# Set defaults.
seq_length = 3

# Get the dataset.
data = DataSet(seq_length=seq_length)
# get the model.
model = Extractor()

# Loop through data.

mydir = '/Users/csprh/tmp/CNNIms/florida2/';
#subdirs1 = [x[0] for x in os.walk('/Users/csprh/tmp/CNNIms/florida2/')]
#subdirs2 = [x[1] for x in os.walk('/Users/csprh/tmp/CNNIms/florida2/')]
max_depth = 0
bottom_most_dirs = []

pbar = tqdm(total=len(bottom_most_dirs))

# data = listOfDirectories;
for thisDir in data.dataLowest:

    # Get the path to the sequence for this video.
    npypath = os.path.join(thisDir, 'seqFeats')

    # Check if we already have it.
    if os.path.isfile(npypath + '.npy'):
        pbar.update(1)


    frames = sorted(glob.glob(os.path.join(thisDir, '*jpg')))
    sequence = []
    for image in frames:
        features = model.extract(image)
        sequence.append(features)

    # Save the sequence.
    np.save(npypath, sequence)

    pbar.update(1)

pbar.close()
