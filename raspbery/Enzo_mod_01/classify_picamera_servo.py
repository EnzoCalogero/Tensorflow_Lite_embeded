from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import io
import time
import numpy as np
import picamera

from time import sleep
from adafruit_servokit import ServoKit

from PIL import Image
from tflite_runtime.interpreter import Interpreter

kit = ServoKit(channels=16)

def load_labels(path):
  with open(path, 'r') as f:
    return {i: line.strip() for i, line in enumerate(f.readlines())}


def set_input_tensor(interpreter, image):
  tensor_index = interpreter.get_input_details()[0]['index']
  input_tensor = interpreter.tensor(tensor_index)()[0]
  input_tensor[:, :] = image


def classify_image(interpreter, image, top_k=1):
  """Returns a sorted array of classification results."""
  set_input_tensor(interpreter, image)
  interpreter.invoke()
  output_details = interpreter.get_output_details()[0]
  #print(output_details['index'])
  #print(interpreter.get_tensor(output_details['index']))
  output = np.squeeze(interpreter.get_tensor(output_details['index']))
  print(output)
  # If the model is quantized (uint8 data), then dequantize the results
  if output_details['dtype'] == np.uint8:
    scale, zero_point = output_details['quantization']
    output = scale * (output - zero_point)

  ordered = np.argpartition(-output, top_k)
  print(ordered[0])
  return [(i, output[i]) for i in ordered[:top_k]]

def servo_ctrl(id=0):
    if (id==3):  #nothing
        kit.servo[0].angle = 10
        kit.servo[1].angle = 10
        kit.servo[2].angle = 10
    elif (id ==2): # closed hand
        kit.servo[0].angle = 10
        kit.servo[1].angle = 10
        kit.servo[2].angle = 90
    elif (id ==1): #more than one finger
        kit.servo[0].angle = 10
        kit.servo[1].angle = 80
        kit.servo[2].angle = 10
    elif (id ==0): #one finger
        kit.servo[0].angle = 80
        kit.servo[1].angle = 10
        kit.servo[2].angle = 10    
    return 0    

def main():
  

  parser = argparse.ArgumentParser(
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument(
      '--model', help='File path of .tflite file.', required=True)
  parser.add_argument(
      '--labels', help='File path of labels file.', required=True)
  args = parser.parse_args()

  labels = load_labels(args.labels)

  interpreter = Interpreter(args.model)
  interpreter.allocate_tensors()
  _, height, width, _ = interpreter.get_input_details()[0]['shape']

  with picamera.PiCamera(resolution=(640, 480), framerate=30) as camera: # it was 30
    camera.start_preview()
    try:
      stream = io.BytesIO()
      for _ in camera.capture_continuous(
          stream, format='jpeg', use_video_port=True):
        stream.seek(0)
        
        img = Image.open(stream).convert('RGB').resize((width, height),
                                                         Image.ANTIALIAS)
        img = np.array(img, dtype=np.float32)
        img = img / 255.

        # Add a batch dimension
        input_data = np.expand_dims(img, axis=0)


        start_time = time.time()
        results = classify_image(interpreter, img)
        elapsed_ms = (time.time() - start_time) * 1000
        label_id, prob = results[0]
        stream.seek(0)
        stream.truncate()
        camera.annotate_text = '%s %.2f\n%.1fms' % (labels[label_id], prob,
                                                    elapsed_ms)
        
        servo_ctrl(id=label_id)
        #time.sleep(5) #Enzo
    finally:
      camera.stop_preview()


if __name__ == '__main__':
  main()
