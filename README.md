# HAB Deep Learning Classifications

This code is for generating classfication scores for HAB databases

There are two basic classification methods:

1. Extract features from each frame with a ConvNet, passing the sequence to an RNN, in a separate network
2. Extract features from each frame with a ConvNet and pass the sequence to an MLP

## Requirements

This code requires you have Keras 2 and TensorFlow 1 or greater installed. Please see the `requirements.txt` file. To ensure you're up to date, run:

`pip install -r requirements.txt`

## Getting the data

The data is extracted using a MATLAB script and deposited into the CNNIms
directory (one jpg per time stamp).

## Extracting features

For the four models (`lstm1`, 'lstm2', 'mlp1' and `mlp2`) features are firstly extracted from each jpg image using the 
`extract\_features.py` script. 

## Training

The actual training (and testing is done using the python file)

trainHAB.py

The training is controlled using the input configuration xml file (e.g. classifyHAB0.xml)
The elements within the configuration file control the training process.  A typical config file is shown below.

```
<confgData>
	<inDir>/mnt/storage/home/csprh/scratch/HAB/CNNIms/florida3/</inDir>
	<dataDir>/mnt/storage/home/csprh/scratch/HAB/DATA3/</dataDir>
	<seqName>seqFeats</seqName>
	<featureLength>20480</featureLength>
	<model>mlp1</model>
	<cnnModel>InceptionV3</cnnModel>
	<seqLength>5</seqLength>
	<batchSize>128</batchSize>
	<epochNumber>2000</epochNumber>
</confgData>
```

inDir: The directory where the jpg images are stored
dataDir: The directory where all the data will be output in the training process
seqName:  CNN output name (numpy file format)
featureLength:  Length of the features output from the CNN
model:  name of model topology: one of mlp1, mlp2, lstm1, lstm2
cnnModel: Name of CNN model (currently ignored)
seqLength: Number of jpg images in each modality (temporal span)
batchSize: tensorflow control
epochNumber: tensorflow control

## TODO

- [ ] Integrate other CNN models (e.g. VGG)
- [ ] Create "whole model" with one CNN for each modality (fine tuned)
- [ ] Try removing more layers of the CNNs

