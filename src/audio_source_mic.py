#!/usr/bin/env python



import numpy
import rospy
from rospy_tutorials.msg import Floats
from rospy.numpy_msg import numpy_msg
import time
import cv2
import speech_recognition as sr

frames = [] 

class audio_source:

    
    def __init__(self, sink):
      
        self.text_pub = rospy.Publisher(sink, numpy_msg(Floats ),queue_size=10, latch=True)
      
        r1 = sr.Recognizer()
        m = sr.Microphone()

        with m as source:
          
          r1.adjust_for_ambient_noise(source)
          self.stop_listening = r1.listen_in_background(m,self.callback2)    
          for _ in range(50): time.sleep(0.1)
          self.stop_listening()      
          while True: time.sleep(0.1)
	
        

    def callback2(recognize, audio1):

          numpydata = numpy.fromstring(audio1.get_raw_data(), dtype=numpy.float32)
          self.text_pub.publish(numpydata)    
 
    

def main():
    
    rospy.init_node('audio_source')
    
  
    
    arg_defaults = {
       
        'sink': '/recognizer/audio'
        }
    args = updateArgs(arg_defaults)
    audio_source(**args)
    try :
       rospy.spin()
    except KeyBoardInterrupt:
      print ("Shutting down")
   

def updateArgs(arg_defaults):
    '''Look up parameters starting in the driver's private parameter space, but
    also searching outer namespaces.  '''
    args = {}
    print ("processing args")
    for name, val in arg_defaults.iteritems():
        full_name = rospy.search_param(name)
        if full_name is None:
            args[name] = val
        else:
            args[name] = rospy.get_param(full_name, val)
            print ("We have args " + val + " value " + args[name])
    return(args)


if __name__ == '__main__':
    main()
