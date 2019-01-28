#!/usr/bin/env python

from geometry_msgs.msg import Twist
from std_msgs.msg import String
import rospy
import sys
import os
import vlc
from Queue import Queue
from threading import Thread,Timer
from pygame import time
from random import randint
import datetime


new=False
index=0
countdown=0

tasources=['/home/enas/catkin_ws/src/multiprocess_render/src/videodog/tadog%d.mp4' %i for i in range(1,12)]

sources=['/home/enas/catkin_ws/src/multiprocess_render/src/videodog/dog%d.mp4' %i for i in range(1,12)]

class display_answer:
    
    def __init__(self,source, sink):


        self.text_sub = rospy.Subscriber(source, String, self.callback)
        self.text_pub = rospy.Publisher(sink, String, queue_size=10, latch=True)
        self.q =Queue()
        self.qtime=Queue()
        self.q.put(sources[0])
        self.qtime.put(994)
        self.playvideos()    

 
    def playit(self):
      global index, countdown 

      url= self.q.get()
      media=self.instance.media_new(url)
      self.player.set_media(media)
      self.player.set_rate(0.9)
      self.player.play()
      media.release()

      if countdown>0:
         countdown=countdown-1
         if countdown==0:
          print "next"
          self.text_pub.publish("next") 
         
      
      time.delay(self.qtime.get())
     

      if self.q.empty():
             

 
           self.q.put(sources[index])

           self.qtime.put(994)

  
           if index>10 or index==10:

               index=0
           else:
               index=index+1



    def playsound(self):

      media=self.instance2.media_new("/home/enas/catkin_ws/src/multiprocess_render/src/audio/say.mp3")
      self.player2.set_media(media)
      self.player2.set_rate(0.9)
      self.player2.play()
      f= open("/home/enas/text.txt","a")
      now = datetime.datetime.now() 
      f.write(now.strftime("rendered audio-video output-%H:%M:%S,"))
      f.close()
      
   
        
    def playvideos(self): 
      global index,countdown,new
      self.instance = vlc.Instance('--input-repeat=-1', '--fullscreen', '--mouse-hide-timeout=0')
      self.player=self.instance.media_player_new()
      self.instance2= vlc.Instance()
      self.player2=self.instance2.media_player_new()

      index=1


      while not self.q.empty():

         worker = Thread(target=self.playit)
         worker.setDaemon(True)
         if new: 
            worker2 = Thread(target=self.playsound)
            worker2.start()
            new=False
         worker.start()
         worker.join()





    def callback(self, data):
        global index,countdown,new
        duration=int(data.data)
        countdown=duration
        new=True 
        print duration
        while duration!=0:

          self.q.put(tasources[(index)])
          self.qtime.put(992)
          duration=duration-1
          index=index+1
          if index>10 or index==10:
             index=0 

       
           
 


def main():
    
    rospy.init_node('display_answer')
   
    arg_defaults = {
        'source': '/answer1/duration1', 
        'sink':'/question/next'    
        }
    args = updateArgs(arg_defaults)
    display_answer(**args)
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
