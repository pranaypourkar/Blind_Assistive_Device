#WITHOUT DOCKER
import tensorflow as tf, sys

import subprocess # for festival
import cv2 # for opencv
import numpy as np
import time # to find time taken by a process



# Loads label file, strips off carriage return
label_lines = [line.rstrip() for line 
                   in tf.gfile.GFile("retrained_labels.txt")]

# Unpersists graph from file
with tf.gfile.FastGFile("retrained_graph.pb", 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')

with tf.Session() as sess:
    
   cap = cv2.VideoCapture(1)
   while(True):
    ret, frame = cap.read()
    #cv2.imshow('frame',frame)
    if cv2.waitKey(3)==27 :
      break;
    cv2.imwrite('/home/pranay/tensorflow/abc.jpg',frame)
    image_path = ('/home/pranay/tensorflow/abc.jpg')
    # Read in the image_data
    image_data = tf.gfile.FastGFile(image_path, 'rb').read()
    # Feed the image_data as input to the graph and get first prediction
    softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
    predictions = sess.run(softmax_tensor, \
             {'DecodeJpeg/contents:0': image_data})
    # Sort to show labels of first prediction in order of confidence
    top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
    for node_id in top_k:

        human_string = label_lines[node_id]
        score = predictions[0][node_id]
        if(score >= 0.85000):
          print('%s (score = %.5f)' % (human_string, score))
          text = human_string    # produce sound*******************************************************
          filename = 'r'
          file=open(filename,'w')
          file.write(text)
          file.close()
          subprocess.call('festival --tts '+filename, shell=True)
        break;# to show one name and score


















 






