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
import sys
from inputXMLConfig import inputXMLConfig

def extract(inDir, seqName, dataDir, seqLength, cnnModel):

    # Get the dataset.

    data = DataSet(seqName, seqLength, inDir, dataDir)
    # get the model.
    model = Extractor(cnnModel)

    # Loop through data.


    max_depth = 0
    bottom_most_dirs = []


    # data = listOfDirectories;
    for thisDir in data.dataLowest:

        # Get the path to the sequence for this video.
        npypath = os.path.join(thisDir, seqName)



        frames = sorted(glob.glob(os.path.join(thisDir, '*jpg')))
        sequence = []
        for image in frames:
            features = model.extract(image)
            sequence.append(features)

        # Save the sequence.
        np.save(npypath, sequence)


    """Main Thread"""
def main(argv):
    """Settings Loaded from Xml Configuration"""
    # model can be one of lstm, mlp, svm
    #import pudb; pu.db

    if (len(argv)==0):
        xmlName = 'classifyHAB1.xml'
    else:
        xmlName = argv[0]

    cnfg = inputXMLConfig(xmlName)
    extract(cnfg.inDir, cnfg.seqName, cnfg.dataDir, cnfg.seqLength, cnfg.cnnModel)


if __name__ == '__main__':
    main(sys.argv[1:])

