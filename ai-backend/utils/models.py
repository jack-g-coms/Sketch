import os
import sys
import tensorflow as tf
from huggingface_hub import hf_hub_download

MODEL = None

def currentModelExists():
    return os.path.isfile('./models/sketch_cnn_model.keras')

def getCurrentModel():
    global MODEL
    if MODEL is None:
        MODEL = tf.keras.models.load_model('models/sketch_cnn_model.keras')
    return MODEL

def downloadCurrentModel():
    os.makedirs('models', exist_ok=True)
    hf_hub_download(
        repo_id='jack311g/sketch_cnn',
        filename='sketch_cnn_model.keras',
        local_dir='models'
    )

if __name__ == '__main__' and len(sys.argv) > 1:
    option = sys.argv[1]
    if option == 'download':
        downloadCurrentModel()