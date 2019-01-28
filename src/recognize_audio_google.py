#!/usr/bin/env python


import numpy
import rospy

import speech_recognition as sr
from rospy_tutorials.msg import Floats
from rospy.numpy_msg import numpy_msg
from std_msgs.msg import String
import datetime


class recognize_audio_google:

  
    def __init__(self, source, sink ):
      
        self.text_pub = rospy.Subscriber(source, numpy_msg(Floats), self.callback)
        self.text_pub = rospy.Publisher(sink, String, queue_size=10, latch=True)
        

    def callback (self,data):
        r = sr.Recognizer()
        with sr.Microphone() as source2:
          
          numpydata = data.data     
          audio=sr.AudioData(numpydata.tobytes(),source2.SAMPLE_RATE, source2.SAMPLE_WIDTH )
          f= open("/home/enas/text.txt","a")
          now = datetime.datetime.now() 
          f.write(now.strftime("audio recognition started-%H:%M:%S, "))
          f.close() 

       

          try:
              self.text=r.recognize_google(audio)
         
         
          except sr.UnknownValueError:
               self.text_pub.publish(" Can you please repeat the question more clearly")
               f= open("/home/enas/errorlog.txt","a")
               now = datetime.datetime.now() 
               f.write(now.strftime("reconinition value error-%H:%M:%S \n  "))
               f.close()
           
          except sr.RequestError as e:
               self.text_pub.publish("I may be disconnected")
               f= open("/home/enas/errorlog.txt","a")
               now = datetime.datetime.now() 
               f.write(now.strftime("reconinition request error-%H:%M:%S \n  "))
               f.close()
          
          else:

            f= open("/home/enas/text.txt","a")
            now = datetime.datetime.now() 
            f.write(now.strftime("audio recognition ended-%H:%M:%S, "))
            f.close()
            self.text_pub.publish(str(self.text))
            print "audio recognized"      

   
def main():
    
    rospy.init_node('recognize_audio_google')
    
  
    
    arg_defaults = {
       
        'source': '/recognizer/audio',
        'sink': '/render1/text1'
        }
    args = updateArgs(arg_defaults)
    recognize_audio_google(**args)
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
