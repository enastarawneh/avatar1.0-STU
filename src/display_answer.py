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


idle=True
state="v"
index=0
countdown=0
countdown2=0

path=['/home/enas/catkin_ws/src/multiprocess_render/src/answer/instance%d/instance1.mp4' %i for i in range(1,6)]


ensources=['/home/enas/catkin_ws/src/multiprocess_render/src/video/engagedv%d.mp4' %i for i in range(1,47)]
ensources2=['/home/enas/catkin_ws/src/multiprocess_render/src/video/engagedx%d.mp4' %i for i in range(1,47)]
ensources3=['/home/enas/catkin_ws/src/multiprocess_render/src/video/engagedy%d.mp4' %i for i in range(1,47)]
ensources4=['/home/enas/catkin_ws/src/multiprocess_render/src/video/engagedz%d.mp4' %i for i in range(1,47)]

sources=['/home/enas/catkin_ws/src/multiprocess_render/src/video/idlearabv%d.mp4' %i for i in range(1,47)]
sources2=['/home/enas/catkin_ws/src/multiprocess_render/src/video/idlearabx%d.mp4' %i for i in range(1,47)]
sources3=['/home/enas/catkin_ws/src/multiprocess_render/src/video/idlearaby%d.mp4' %i for i in range(1,47)]
sources4=['/home/enas/catkin_ws/src/multiprocess_render/src/video/idlearabz%d.mp4' %i for i in range(1,47)]

    
umsources=['/home/enas/catkin_ws/src/multiprocess_render/src/video/umengagedv%d.mp4' %i for i in range(1,93)]
umsources2=['/home/enas/catkin_ws/src/multiprocess_render/src/video/umengagedx%d.mp4' %i for i in range(1,93)]
umsources3=['/home/enas/catkin_ws/src/multiprocess_render/src/video/umengagedy%d.mp4' %i for i in range(1,93)]
umsources4=['/home/enas/catkin_ws/src/multiprocess_render/src/video/umengagedz%d.mp4' %i for i in range(1,93)]


ahsources=['/home/enas/catkin_ws/src/multiprocess_render/src/video/ahengagedv%d.mp4' %i for i in range(1,93)]
ahsources2=['/home/enas/catkin_ws/src/multiprocess_render/src/video/ahengagedx%d.mp4' %i for i in range(1,93)]
ahsources3=['/home/enas/catkin_ws/src/multiprocess_render/src/video/ahengagedy%d.mp4' %i for i in range(1,93)]
ahsources4=['/home/enas/catkin_ws/src/multiprocess_render/src/video/ahengagedz%d.mp4' %i for i in range(1,93)]

brsources=['/home/enas/catkin_ws/src/multiprocess_render/src/video/bridgeengagedv%d.mp4' %i for i in range(1,47)]
brsources2=['/home/enas/catkin_ws/src/multiprocess_render/src/video/bridgeengagedx%d.mp4' %i for i in range(1,47)]
brsources3=['/home/enas/catkin_ws/src/multiprocess_render/src/video/bridgeengagedy%d.mp4' %i for i in range(1,47)]
brsources4=['/home/enas/catkin_ws/src/multiprocess_render/src/video/bridgeengagedz%d.mp4' %i for i in range(1,47)]

class display_answer:
    
    def __init__(self,source,sink,sink2):

        self.text_pub = rospy.Publisher(sink, String, queue_size=10, latch=True)
        self.text_pub2 = rospy.Publisher(sink2, String, queue_size=10, latch=True)
        self.text_sub = rospy.Subscriber(source, String, self.callback)

        self.q =Queue()
        self.qtime=Queue()
        self.q.put(sources[0])
        self.qtime.put(994)
        self.playvideos()    

 
    def playit(self):
      global index,state, idle, countdown,countdown2

      url= self.q.get()
      media=self.instance.media_new(url)
      self.player.set_media(media)
      self.player.set_rate(0.9)
      self.player.play()
      media.release()
      if countdown>0:
         countdown=countdown-1 
      if countdown2>0:
         countdown2=countdown2-1
         if countdown2==0:
          print "next"
          self.text_pub2.publish("next") 
         
      
      time.delay(self.qtime.get())
     

      if self.q.empty():
             
           if (index==0 or index==10 or index==18 or index==24 or index==30) and (state=="x" or state=="v") :
             if (randint(0, 1))==1:     
                state="x"
             else:
                state="v"
           if (index==3 or index==8 or index==15 or index==22 or index==34) and (state=="x" or state=="y"): 
             if (randint(0, 1))==1:     
                state="y"
             else:
                state="x"
           if (index==6 or index==12 or index==20 or index==28 or index==36 ) and (state=="z" or state=="y"): 
             if (randint(0, 1))==1:     
                state="z"
             else:
                state="y"
             

           if state=="x":
               
                    if idle==True:
                      self.q.put(sources2[index])
                    else:
                      self.q.put(ensources2[index]) 

                    self.qtime.put(994)
           elif state=="v":              

                    if idle==True:
                      self.q.put(sources[index])
                    else:
                      self.q.put(ensources[index]) 


                    self.qtime.put(994)
           elif state=="y":               
                    if idle==True:
                      self.q.put(sources3[index])
                    else:
                      self.q.put(ensources3[index]) 

                    self.qtime.put(994)
           elif state=="z":
               
                    if idle==True:
                      self.q.put(sources4[index])
                    else:
                      self.q.put(ensources4[index]) 


                    self.qtime.put(994)

  
           if index>39 or index==39:

                index=0
           else:
               index=index+1

           self.text_pub.publish(str(index)+","+state)

    def playsound(self):
      time.delay(1000)
      media=self.instance2.media_new("/home/enas/catkin_ws/src/multiprocess_render/src/audio/say.mp3")
      self.player2.set_media(media)
      self.player2.set_rate(0.9)
      self.player2.play()
      f= open("/home/enas/text.txt","a")
      now = datetime.datetime.now() 
      f.write(now.strftime("rendered audio-video output-%H:%M:%S,"))
      f.close()
      
   
        
    def playvideos(self): 
      global index,countdown
      self.instance = vlc.Instance('--input-repeat=-1', '--fullscreen', '--mouse-hide-timeout=0')
      self.player=self.instance.media_player_new()
      self.instance2= vlc.Instance()
      self.player2=self.instance2.media_player_new()

      index=1


      while not self.q.empty():

         worker = Thread(target=self.playit)
         worker.setDaemon(True)
         if countdown==1: 
           worker2 = Thread(target=self.playsound)
           worker2.start()
         worker.start()
         worker.join()





    def callback(self, data):
        global index,idle, countdown, countdown2
        countdown=10
        countdown2=23
        if state=="x":
                  if idle:
                    self.q.put(brsources2[index])
                  else:
                    self.q.put(ensources2[index]) 
                  self.qtime.put(994)
                  self.q.put(umsources2[(index+1)*2])
                  self.qtime.put(1980)
                  self.q.put(ahsources2[((index+1)*2)+2])
                  self.qtime.put(1980)
                  self.q.put(ahsources2[((index+1)*2)+4])
                  self.qtime.put(1980)
                  self.q.put(ensources2[index+4])
                  self.qtime.put(994)
                  self.q.put(ensources2[index+5])
                  self.qtime.put(994)
                  self.q.put(ensources2[index+6])
                  self.qtime.put(994)
                  self.q.put(ensources2[index+7])
                  self.qtime.put(994)
                  self.q.put(umsources2[(index+8)*2])
                  self.qtime.put(1980)
                  self.q.put(ahsources2[((index+8)*2)+2])
                  self.qtime.put(1980)
                  self.q.put(path[0])
                  self.qtime.put(int((float(4)/12)*994))
                  self.q.put(path[1])
                  self.qtime.put(int((float(6)/12)*994))
                  self.q.put(path[2])
                  self.qtime.put(int((float(8)/12)*994))
                  self.q.put(path[3])
                  self.qtime.put(int((float(13)/12)*994))
                  self.q.put(path[4])
                  self.qtime.put(int((float(19)/12)*994))


                  index=index+12
                  if index>39 or index==39:
                      index=0 

        elif state=="v":              
                   if idle:
                    self.q.put(brsources[index])
                   else:
                    self.q.put(ensources[index])
                   self.qtime.put(994) 
                   self.q.put(umsources[(index+1)*2])
                   self.qtime.put(1980)
                   self.q.put(ahsources[((index+1)*2)+2])
                   self.qtime.put(1980)
                   self.q.put(ahsources[((index+1)*2)+4])
                   self.qtime.put(1980)
                   self.q.put(ensources[index+4])
                   self.qtime.put(994)
                   self.q.put(ensources[index+5])
                   self.qtime.put(994)
                   self.q.put(ensources[index+6])
                   self.qtime.put(994)
                   self.q.put(ensources[index+7])
                   self.qtime.put(994)
                   self.q.put(umsources[(index+8)*2])
                   self.qtime.put(1980)
                   self.q.put(ahsources[((index+8)*2)+2])
                   self.qtime.put(1980)
                   self.q.put(path[0])
                   self.qtime.put(int((float(4)/12)*994))
                   self.q.put(path[1])
                   self.qtime.put(int((float(6)/12)*994))
                   self.q.put(path[2])
                   self.qtime.put(int((float(8)/12)*994))
                   self.q.put(path[3])
                   self.qtime.put(int((float(13)/12)*994))
                   self.q.put(path[4])
                   self.qtime.put(int((float(19)/12)*994))
                   index=index+12
                   if index>39 or index==39:
                      index=0 

        elif state=="y":
                   if idle:
                    self.q.put(brsources3[index])
                   else:
                    self.q.put(ensources3[index])
                   self.qtime.put(994)               
                   self.q.put(umsources3[(index+1)*2])
                   self.qtime.put(1980)
                   self.q.put(ahsources3[((index+1)*2)+2])
                   self.qtime.put(1980)
                   self.q.put(ahsources3[((index+1)*2)+4])
                   self.qtime.put(1980)
                   self.q.put(ensources3[index+4])
                   self.qtime.put(994)
                   self.q.put(ensources3[index+5])
                   self.qtime.put(994)
                   self.q.put(ensources3[index+6])
                   self.qtime.put(994)
                   self.q.put(ensources3[index+7])
                   self.qtime.put(994)
                   self.q.put(umsources3[(index+8)*2])
                   self.qtime.put(1980)
                   self.q.put(ahsources3[((index+8)*2)+2])
                   self.qtime.put(1980)
                   self.q.put(path[0])
                   self.qtime.put(int((float(4)/12)*994))
                   self.q.put(path[1])
                   self.qtime.put(int((float(6)/12)*994))
                   self.q.put(path[2])
                   self.qtime.put(int((float(8)/12)*994))
                   self.q.put(path[3])
                   self.qtime.put(int((float(13)/12)*994))
                   self.q.put(path[4])
                   self.qtime.put(int((float(19)/12)*994))
                   index=index+12
                   if index>39 or index==39:
                      index=0  

        elif state=="z":
                   if idle:
                    self.q.put(brsources4[index])
                   else:
                    self.q.put(ensources4[index])
                   self.qtime.put(994)               
                   self.q.put(umsources4[(index+1)*2])
                   self.qtime.put(1980)
                   self.q.put(ahsources4[((index+1)*2)+2])
                   self.qtime.put(1980)
                   self.q.put(ahsources4[((index+1)*2)+4])
                   self.qtime.put(1980)
                   self.q.put(ensources4[index+4])
                   self.qtime.put(994)
                   self.q.put(ensources4[index+5])
                   self.qtime.put(994)
                   self.q.put(ensources4[index+6])
                   self.qtime.put(994)
                   self.q.put(ensources4[index+7])
                   self.qtime.put(994)
                   self.q.put(umsources3[(index+8)*2])
                   self.qtime.put(1980)
                   self.q.put(ahsources3[((index+8)*2)+2])
                   self.qtime.put(1980)               
                   self.q.put(path[0])
                   self.qtime.put(int((float(4)/12)*994))
                   self.q.put(path[1])
                   self.qtime.put(int((float(6)/12)*994))
                   self.q.put(path[2])
                   self.qtime.put(int((float(8)/12)*994))
                   self.q.put(path[3])
                   self.qtime.put(int((float(13)/12)*994))
                   self.q.put(path[4])
                   self.qtime.put(int((float(19)/12)*994))
                   index=index+12
                   if index>39 or index==39:
                      index=0 
           
        idle=False   
        print "starting now.........................................."+ str(datetime.datetime.now()) 


def main():
    
    rospy.init_node('display_answer')
   
    arg_defaults = {
        'source': '/render1/text1',
        'sink2':'/question/next',
        'sink':'/display/index' 
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
