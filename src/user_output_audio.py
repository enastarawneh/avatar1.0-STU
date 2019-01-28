#!/usr/bin/env python


from std_msgs.msg import String
import rospy
import sys
from PyQt4 import QtGui
from playsound import playsound
import datetime



class user_output_text:

    
    def __init__(self,source,sink):
      
        self.text_sub = rospy.Subscriber(source, String, self.callback)
        self.text_pub = rospy.Publisher(sink, String, queue_size=10, latch=True)
        self.initUI()



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
     with open('output2.mp3', 'wb') as out:
        out.write(response.audio_content)
     self.win.label.setText("audio playing")
     f= open("/home/enas/text.txt","a")
     now = datetime.datetime.now() 
     f.write(now.strftime("response audio output-%H:%M:%S"))
     f.close()  
     playsound('output2.mp3')
     self.text_pub.publish("next")   
     self.win.label.setText("Next Question") 
      
    def initUI(self):      
        self.app = QtGui.QApplication([])
        self.win = QtGui.QWidget()
        self.win.setStyleSheet("background-color:black; color:white; font-family:'Times New Roman';")

        self.win.label = QtGui.QLabel("Ask a question", self.win)
        self.win.label.move(50, 50)
        self.win.label.setFixedWidth(700)
        #self.win.le = QtGui.QLineEdit(self.win)
        #self.win.le.setFixedWidth(300)
        #self.win.le.move(150, 50)
 
        self.win.label.setStyleSheet("font-size:30px")
        self.win.setGeometry(700, 300, 850, 250)
        self.win.setWindowTitle('Answer')
        self.win.show()
        self.app.exec_()

        

        
   
    def callback(self, data):  
          
          self.synthesize_text(data.data)
          
          
 


def main():
    
    rospy.init_node('user_output_text')
    
  
    
    arg_defaults = {
        'source': '/answer1/text1',
        'sink':'/question/next'
        }
    args = updateArgs(arg_defaults)
    user_output_text(**args)
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
