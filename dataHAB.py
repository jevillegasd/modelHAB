"""
Class for managing our data.
"""
import csv
import numpy as np
import random
import glob
import os.path
import sys
import operator
import threading
from processor import process_image
from keras.utils import to_categorical
import os.path

class threadsafe_iterator:
    def __init__(self, iterator):
        self.iterator = iterator
        self.lock = threading.Lock()

    def __iter__(self):
        return self

    def __next__(self):
        with self.lock:
            return next(self.iterator)

def threadsafe_generator(func):
    """Decorator"""
    def gen(*a, **kw):
        return threadsafe_iterator(func(*a, **kw))
    return gen

class DataSet():

    def __init__(self, seqName, seq_length, inDir, dataDir,  image_shape=(224, 224, 3)):

        self.seq_length = seq_length
        self.max_frames = 300  # max number of frames a video can have for us to use it

        self.inDir = inDir
        self.dataDir = dataDir
        self.seqName = seqName
        # Get the data.
        self.dataLowest = self.get_data(self.inDir)
        self.data = self.extract_data(self.dataLowest)
        self.image_shape = image_shape

    @staticmethod
    def get_data(inDir):
        """Load our data from file."""

        max_depth = 0
        bottom_most_dirs = []
        for dirpath, dirnames, filenames in os.walk(inDir):
            depth = len(dirpath.split(os.sep))
            if max_depth < depth:
                max_depth = depth
                bottom_most_dirs = [dirpath]
            elif max_depth == depth:
                bottom_most_dirs.append(dirpath)

        return bottom_most_dirs

    @staticmethod
    def extract_data(dataLowest):
        """ Get rid of last layer of dataLowest and put into data """
        output = []
        bottom_most_dirs = []
        for x in dataLowest:
                head, tail = os.path.split(x)
                bottom_most_dirs.append(head)

        for x in bottom_most_dirs:
            if x not in output:
                output.append(x)

        return output

    def get_class_one_hot(self, path_str):
        """Given a class as a string, return its number in the classes
        list. This lets us encode and one-hot it for training."""
        # Encode it first.
        parts = path_str.split(os.path.sep)

        # Now one-hot it.
        label_hot = to_categorical(int(parts[-2]), 2)

        assert len(label_hot) == 2

        return label_hot

    def split_train_test(self):
        """Split the data into train and test groups."""
        train = []
        test = []
        thisall = []

        for item in self.data:
            parts = item.split(os.path.sep)
            if parts[-3] == 'Train':
                train.append(item)
            else:
                test.append(item)
            thisall.append(item)
        return train, test, thisall


    def get_all_sequences_in_memory(self, train_test, data_type):
        """
        This is a mirror of our generator, but attempts to load everything into
        memory so we can train way faster.
        """
        # Get the right dataset.
        train, test, thisall = self.split_train_test()
        if train_test == 'train':
            data = train
            print("Loading %d samples into memory for training." % len(data))
        elif train_test == 'test':
            data = test
            print("Loading %d samples into memory for training." % len(data))
        elif train_test == 'all':
            data = thisall
            print("Loading all %d samples into memory" % len(thisall))

        X, y = [], []
        for sample in data:

            sequence = self.get_extracted_sequenceAllMods(data_type, sample)

            X.append(sequence)
            y.append(self.get_class_one_hot(sample))

        return np.array(X), np.array(y)

    @threadsafe_generator
    def frame_generator(self, batch_size, train_test, data_type):
        """Return a generator that we can use to train on. There are
        a couple different things we can return:

        data_type: 'features', 'images'
        """
        # Get the right dataset for the generator.
        train, test = self.split_train_test()
        data = train if train_test == 'train' else test

        print("Creating %s generator with %d samples." % (train_test, len(data)))

        while 1:
            X, y = [], []

            # Generate batch_size samples.
            for _ in range(batch_size):
                # Reset to be safe.
                sequence = None

                # Get a random sample.
                sample = random.choice(data)


                # Get the sequence from disk.
                sequence = self.get_extracted_sequenceAllMods(data_type, sample)

                if sequence is None:
                    raise ValueError("Can't find sequence. Did you generate them?")

                X.append(sequence)
                y.append(self.get_class_one_hot(sample))

            yield np.array(X), np.array(y)

    def get_extracted_sequenceAllMods(self, data_type, filename):
        """Get the saved extracted features."""
        #filename = sample[2]

        thisreturn = []
        for i in range(1,11):

            thispath = filename + '/' + str(i) + '/' +  self.seqName + '.npy'
            thisfeats = np.load(thispath)
            #if os.path.isfile(path):
            #    return np.load(path)
            #else:
            #    return None
            if i == 1 :
                thisreturn = thisfeats
            else:
                thisreturn = np.concatenate((thisreturn, thisfeats), axis=1)
        return thisreturn

    def get_extracted_sequence(self, data_type, filename):
        """Get the saved extracted features."""
        #filename = sample[2]

        path = filename + '/8/' + self.seqName + '.npy'
        if os.path.isfile(path):
            return np.load(path)
        else:
            return None

