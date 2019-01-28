#!/usr/bin/env python


from std_msgs.msg import String
import rospy
import sys
import os
import types
from num2words import num2words
import re

newone=" " 


class file_store:

    
    def __init__(self, source, sink):
        global newindex
        self.text_sub = rospy.Subscriber(source, String, self.callback)
        self.text_pub = rospy.Publisher(sink, String, queue_size=10, latch=False)
       


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
     
     
         
             
        
    def callback(self, data):
     global newone
     if  newone != str(data.data): 
        newone=str(data.data)
        words = newone.split()
        for word in words:
         if re.search(r'\d+.?\d*', word):
            newone2=newone.replace(word,num2words(word))
            newone2=newone2.replace(" point zero","")
            newone2=newone2.replace("-"," ")
        text_file = open("/home/enas/catkin_ws/src/multiprocess_render/src/txtscript/script1.txt", "w")
        text_file.write(str(newone2))
        text_file.close()
        dist1="/home/enas/catkin_ws/src/multiprocess_render/src/txtscript/script1.txt"
        self.synthesize_text(newone)
        os.system("gcloud compute scp  /home/enas/catkin_ws/src/multiprocess_render/src/txtscript/script1.txt instance-5:~/guy-engaged1/") 
        
        self.text_pub.publish(str(newone)) 

       



def main():
   
    rospy.init_node('file_store')
   
    arg_defaults = {
        'source': '/answer1/text1',
        'sink': '/render1/text2',
        }
    args = updateArgs(arg_defaults)
    file_store(**args)
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
