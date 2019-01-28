#!/usr/bin/env python


from std_msgs.msg import String
import numpy
import rospy
from rospy_tutorials.msg import Floats
from rospy.numpy_msg import numpy_msg
import cv2
import speech_recognition as sr
import datetime
import wave


class audio_source:

    
    def __init__(self, source, sink):

        self.text_sub = rospy.Subscriber(source, String, self.callback2)
        self.text_pub = rospy.Publisher(sink, numpy_msg(Floats ),queue_size=10, latch=True)
        self.callback()

    def callback (self):
       
        r1 = sr.Recognizer()  
        with sr.Microphone() as source:
          print "speak now"
          r1.adjust_for_ambient_noise(source)
          f= open("/home/enas/text.txt","a")
          now = datetime.datetime.now() 
          f.write("\n"+now.strftime("start listening-%H:%M:%S, "))
          f.close()
          audio1 = r1.listen(source)    
          numpydata = numpy.fromstring(audio1.get_raw_data(), dtype=numpy.float32)
          self.text_pub.publish(numpydata)
          print "sent audio" 
          wav_writer = wave.open('wav_file.wav',"wb")
          wav_writer.setframerate(source.SAMPLE_RATE)
          wav_writer.setsampwidth(source.SAMPLE_WIDTH)
          wav_writer.setnchannels(1)
          wav_writer.writeframes(audio1.get_raw_data())

          
          f= open("/home/enas/text.txt","a")
          now = datetime.datetime.now() 
          f.write(now.strftime("speech heard-%H:%M:%S, input time-"+ str( wav_writer.getnframes()/ wav_writer.getframerate())+", "))
          f.close()
          wav_writer.close()

 
    def callback2 (self, data):   
        self.callback()
          


      
   
def main():
    
    rospy.init_node('audio_source')
    
  
    
    arg_defaults = {

        'source': '/question/next',     
        'sink': '/recognizer/audio',

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
