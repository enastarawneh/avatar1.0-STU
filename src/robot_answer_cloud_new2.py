#!/usr/bin/env python


from std_msgs.msg import String
import rospy
import sys
import subprocess32
newindex=0
from tinytag import TinyTag
import datetime
import os
from num2words import num2words
import re
import math

class robot_answer:

    
    def __init__(self,sink, source1):
        self.text_pub = rospy.Publisher(sink, String, queue_size=10, latch=True) 
        self.text_sub = rospy.Subscriber(source1, String, self.callback)
     
    
 
    def synthesize_text(self,text):
     """Synthesizes speech from the input string of text."""
     from google.cloud import texttospeech
     client = texttospeech.TextToSpeechClient()

     input_text = texttospeech.types.SynthesisInput(text=text)

     # Note: the voice can also be specified by name.
     # Names of voices can be retrieved with client.list_voices().
     voice = texttospeech.types.VoiceSelectionParams(
        language_code='en-US',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.MALE, name="en-US-Wavenet-A")

     audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3,speaking_rate=1)

     response = client.synthesize_speech(input_text, voice, audio_config)
     
     # The response's audio_content is binary.
     with open('/home/enas/catkin_ws/src/multiprocess_render/src/audio/say.mp3', 'wb') as out:
        out.write(response.audio_content)
     f= open("/home/enas/text.txt","a")
     now = datetime.datetime.now() 
     f.write(now.strftime("response audio output-%H:%M:%S,"))
     f.close()  




    def callback(self, data):
       global index, state
       newone=str(data.data)
       words = newone.split()

       
       self.synthesize_text(data.data)
       tag = TinyTag.get('/home/enas/catkin_ws/src/multiprocess_render/src/audio/say.mp3')
       duration=int(math.ceil(tag.duration))
       self.text_pub.publish(str(duration)) 

   
      
       


def main():
   
    rospy.init_node('robot_answer')
   
    arg_defaults = {
        'sink':'/answer1/duration',
        'source1': '/answer1/text1'
        }
    args = updateArgs(arg_defaults)
    robot_answer(**args)
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
            print ("We have args " + val + " value " + str(args[name]))
    return(args)


if __name__ == '__main__':
    main()
