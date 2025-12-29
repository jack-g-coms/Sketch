import sys
import os
import tensorflow as tf
from utils.preprocess import FIXED_SIZE
import utils.models as models
import utils.dataset as dataset

inputs, labels = dataset.getInputsAndLabels(dataset.PROCESSED_DIRECTORY)
model = None

if models.currentModelExists():
    model = models.getCurrentModel()
else:
    model = tf.keras.Sequential([
        tf.keras.layers.Conv2D(32, (3,3), activation='relu', padding='same', input_shape=(FIXED_SIZE[0], FIXED_SIZE[1], 1)),
        tf.keras.layers.MaxPooling2D((2,2)),
        
        tf.keras.layers.Conv2D(64, (3,3), activation='relu', padding='same'),
        tf.keras.layers.MaxPooling2D((2,2)),

        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(len(labels))
    ])
    model.compile(
        optimizer='adam', 
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), 
        metrics=['accuracy']
    )

def train():
    testInputs, testLabels = dataset.getInputsAndLabels(dataset.TESTING_DIRECTORY)

    model.fit(inputs, labels, batch_size=32, epochs=10, shuffle=True)
    test_loss, test_acc = model.evaluate(testInputs, testLabels, verbose=2)

    print(f'\nTest Accuracy: {test_acc}')

    model.save('models/sketch_cnn_model.keras')

if __name__ == '__main__' and len(sys.argv) > 1:
    option = sys.argv[1]
    if option == 'train':
        train()