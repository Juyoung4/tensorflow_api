#!/usr/bin/env python
# coding: utf-8

# In[5]:


import tempfile
import os
import tensorflow as tf
import numpy as np
from tensorflow import keras
#import tensorflow_model_optimization as tfmot
import argparse
from tensorflow.python.keras.callbacks import Callback
from tensorflow.python.lib.io import file_io
import json


# 모델 사이즈를 측정하기 위한 함수
def get_gzipped_model_size(file):
  # Returns size of gzipped model, in bytes.
    import os
    import zipfile

    _, zipped_file = tempfile.mkstemp('.zip')
    with zipfile.ZipFile(zipped_file, 'w', compression=zipfile.ZIP_DEFLATED) as f:
        f.write(file)

    return os.path.getsize(zipped_file)

class Mnist(object):
    def train(self):

        parser = argparse.ArgumentParser()
        parser.add_argument('--learning_rate', required=False, type=float, default=0.001)
        parser.add_argument('--dropout_rate', required=False, type=float, default=0.3)  
        parser.add_argument('--model_path', required=False, default='/result',type = str)  #/saved_model
        parser.add_argument('--model_version', required=False, default='/base_model.h5',type = str)#test2/Base_model.h5
        args = parser.parse_args()



        # Load MNIST dataset
        mnist = tf.keras.datasets.mnist
        (train_images, train_labels), (test_images, test_labels) = mnist.load_data()

        # Normalize the input image so that each pixel value is between 0 to 1.
        train_images = train_images / 255.0
        test_images = test_images / 255.0
        # Define the model architecture
        model = tf.keras.Sequential([
          tf.keras.layers.InputLayer(input_shape=(28, 28)),
          tf.keras.layers.Reshape(target_shape=(28, 28, 1)),
          tf.keras.layers.Conv2D(filters=12, kernel_size=(3, 3), activation='relu'),
          tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
          tf.keras.layers.Flatten(),
          tf.keras.layers.Dense(10)
        ])
        
        model.summary()

        # Train the digit classification model
        model.compile(optimizer='adam',
                      loss=tf.keras.losses.SparseCategoricalCrossentropy(
                          from_logits=True),
                      metrics=['accuracy'])
        model.fit(
          train_images,
          train_labels,
          epochs=5,
          validation_data=(test_images, test_labels),
        )
        #model.fit(x_train, y_train, epochs=5,callbacks=[KatibMetricLog()])

        
        results = model.evaluate(test_images, test_labels, batch_size=128)
        print('test loss, test acc:', results)
        
        _, model_accuracy = model.evaluate(test_images, test_labels, verbose=0)
        print("Base model accuracy : ", model_accuracy)
        
        
        loss = results[0]
        accuracy = results[1]
        metrics = {
            'metrics': [{
                'name': 'accuracy',
                'numberValue': float(accuracy),
                'format': "PERCENTAGE",
            }, {
                'name': 'loss',
                'numberValue': float(loss),
                'format': "RAW",
            }]
        }
        
        with file_io.FileIO('/mlpipeline-metrics.json', 'w') as f:
            json.dump(metrics, f)
   
        tf.keras.models.save_model(model, args.model_path+args.model_version, include_optimizer=False) #os.getcwd()+'/'+args.model_version.split('/')[1]
        print("Base model size: ",get_gzipped_model_size(args.model_path+args.model_version))


def fairing_run():
    CONTAINER_REGISTRY = 'khw2126'

    namespace = 'admin'
    job_name = f'mnist-job-{uuid.uuid4().hex[:4]}'


    fairing.config.set_builder('append', registry=CONTAINER_REGISTRY, image_name="mnist-simple",base_image="khw2126/tensorflow-2.0.0-notebook-gpu:3.0.0")

    #fairing.config.set_deployer('job', namespace=namespace, job_name=job_name, cleanup=False, stream_log=True)
    
    fairing.config.set_deployer('job', namespace=namespace, job_name=job_name, cleanup=False, stream_log=True,
                                pod_spec_mutators=[
                                    k8s_utils.mounting_pvc(pvc_name="workspace-hufsice", 
                                                           pvc_mount_path="/result")])

    fairing.config.run()
    
if __name__ == '__main__':
    if os.getenv('FAIRING_RUNTIME', None) is None:
        import uuid
        from kubeflow import fairing
        from kubeflow.fairing.kubernetes import utils as k8s_utils
        fairing_run()
    else:
        remote_train = Mnist()
        remote_train.train()
        





# In[ ]:




