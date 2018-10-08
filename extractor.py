from keras.preprocessing import image
from keras.applications.inception_v3 import InceptionV3
from keras.applications.inception_v3 import preprocess_input as inception_v3_preprocessor
from keras.applications.inception_resnet_v2 import InceptionResNetV2
from keras.applications.inception_resnet_v2 import preprocess_input as  inception_resnet_v2_preprocessor
from keras.applications.vgg19 import VGG19
from keras.applications.vgg19 import preprocess_input as vgg19_preprocessor
#from keras.applications.inception_v3 import preprocess_input as inception_v3_preprocessor
from keras.models import Model, load_model
from keras.layers import Input
import numpy as np

class Extractor():
    def __init__(self, cnnModel, weights=None):
        """Either load pretrained from imagenet, or load our saved
        weights from our own training."""


        self.weights = weights  # so we can check elsewhere which model

        if weights is None:
            if cnnModel == 'InceptionV3':
                # Get model with pretrained weights.
                base_model = InceptionV3(
                    weights='imagenet',
                    include_top=True
                )

                # We'll extract features at the final pool layer.
                self.model = Model(
                    inputs=base_model.input,
                    outputs=base_model.get_layer('avg_pool').output
                )
                self.target_size = (299,299)
                self.preprocess_input = inception_v3_preprocessor
            elif cnnModel == 'VGG19':
                # Get model with pretrained weights.
                base_model = VGG19(
                    weights='imagenet',
                    include_top=True
                )

                # We'll extract features at the final pool layer.
                self.model = Model(
                    inputs=base_model.input,
                    outputs=base_model.get_layer('fc2').output
                )
                self.target_size = (224,224)
                self.preprocess_input = vgg19_preprocessor
            elif cnnModel == 'InceptionResNetV2':
                # Get model with pretrained weights.
                base_model = InceptionResNetV2(
                    weights='imagenet',
                    include_top=True
                )

                # We'll extract features at the final pool layer.
                self.model = Model(
                    inputs=base_model.input,
                    outputs=base_model.get_layer('avg_pool').output
                )
                self.target_size = (299,299)
                self.preprocess_input = inception_resnet_v2_preprocessor
        else:
            # Load the model first.
            self.model = load_model(weights)

            # Then remove the top so we get features not predictions.
            # From: https://github.com/fchollet/keras/issues/2371
            self.model.layers.pop()
            self.model.layers.pop()  # two pops to get to pool layer
            self.model.outputs = [self.model.layers[-1].output]
            self.model.output_layers = [self.model.layers[-1]]
            self.model.layers[-1].outbound_nodes = []

    def extract(self, image_path):
        img = image.load_img(image_path, target_size=self.target_size)
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = self.preprocess_input(x)

        # Get the prediction.
        features = self.model.predict(x)

        if self.weights is None:
            # For imagenet/default network:
            features = features[0]
        else:
            # For loaded network:
            features = features[0]

        return features
