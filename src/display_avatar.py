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

yeahsources=['/home/enas/catkin_ws/src/multiprocess_render/src/userstudy/yeahguy%d.mp4' %i for i in range(1,93)]
yessources=['/home/enas/catkin_ws/src/multiprocess_render/src/userstudy/yesguy%d.mp4' %i for i in range(1,93)]
suresources=['/home/enas/catkin_ws/src/multiprocess_render/src/userstudy/sureguy%d.mp4' %i for i in range(1,93)]
ummsources=['/home/enas/catkin_ws/src/multiprocess_render/src/userstudy/umguy%d.mp4' %i for i in range(1,93)]
ahsources=['/home/enas/catkin_ws/src/multiprocess_render/src/userstudy/ahguy%d.mp4' %i for i in range(1,93)]
ohsources=['/home/enas/catkin_ws/src/multiprocess_render/src/userstudy/ohguy%d.mp4' %i for i in range(1,93)]

tasources=['/home/enas/catkin_ws/src/multiprocess_render/src/userstudy/taguy%d.mp4' %i for i in range(1,93)]

sources=['/home/enas/catkin_ws/src/multiprocess_render/src/userstudy/guy%d.mp4' %i for i in range(1,93)]

class display_answer:
    
    def __init__(self,source, source1, sink):

        self.text_sub1 = rospy.Subscriber(source1, String, self.callback1)
        self.text_sub = rospy.Subscriber(source, String, self.callback)
        self.text_pub = rospy.Publisher(sink, String, queue_size=10, latch=True)
        self.q =Queue()
        self.qtime=Queue()
        self.q.put(sources[0])
        self.qtime.put(1000)
        self.playvideos()    

 
    def playit(self):
      global index, countdown 

      url= self.q.get()
      media=self.instance.media_new(url)
      self.player.set_media(media)
      self.player.set_rate(0.93)
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

           self.qtime.put(1000)

  
           if index>91 or index==91:

               index=0
           else:
               index=index+1



    def playsound(self):
       
      media=self.instance2.media_new("/home/enas/catkin_ws/src/multiprocess_render/src/audio/say.mp3")
      self.player2.set_media(media)
      self.player2.set_rate(0.90)
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
        duration=duration-1 
        print duration
        while duration!=0:

          self.q.put(tasources[(index)])
          self.qtime.put(1000)
          duration=duration-1
          index=index+1
          if index>91 or index==91:
             index=0 

       
    def callback1(self, data):           
        global index,countdown,new
        x=randint(0,5)
        y=randint(0,5)
        #if x==0:  
         #self.q.put(ahsources[(index)])
        if x==1:  
         self.q.put(ummsources[(index)])
        if x==2:  
         self.q.put(yeahsources[(index)])
        if x==3:  
         self.q.put(yessources[(index)])
        if x==4:  
         self.q.put(suresources[(index)])
        #if x==5:  
         #self.q.put(ohsources[(index)])
        self.qtime.put(1000)
        index=index+1
        if index>92 or index==92:
          index=0
        #if y==0:  
         #self.q.put(ahsources[(index)])
        if y==1:  
         self.q.put(ummsources[(index)])
        if y==2:  
         self.q.put(yeahsources[(index)])
        if y==3:  
         self.q.put(yessources[(index)])
        if y==4:  
         self.q.put(suresources[(index)])
        #if y==5:  
         #self.q.put(ohsources[(index)])
        self.qtime.put(1000)
        index=index+1
        if index>91 or index==91:
             index=0


def main():
    
    rospy.init_node('display_answer')
   
    arg_defaults = {
        'source': '/answer1/duration1',
        'source1': '/render1/text1', 
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
