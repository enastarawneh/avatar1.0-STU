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
mlist=[]

lionfish=['/home/enas/catkin_ws/src/multiprocess_render/src/video_women/zero.mp4',
'/home/enas/catkin_ws/src/multiprocess_render/src/video_women/one.mp4',
'/home/enas/catkin_ws/src/multiprocess_render/src/video_women/two.mp4',
'/home/enas/catkin_ws/src/multiprocess_render/src/video_women/three.mp4',
'/home/enas/catkin_ws/src/multiprocess_render/src/video_women/four.mp4',
'/home/enas/catkin_ws/src/multiprocess_render/src/video_women/five.mp4',
'/home/enas/catkin_ws/src/multiprocess_render/src/video_women/six.mp4',
'/home/enas/catkin_ws/src/multiprocess_render/src/video_women/seven.mp4',
'/home/enas/catkin_ws/src/multiprocess_render/src/video_women/eight.mp4',
'/home/enas/catkin_ws/src/multiprocess_render/src/video_women/nine.mp4',
'/home/enas/catkin_ws/src/multiprocess_render/src/video_women/ten.mp4',
'/home/enas/catkin_ws/src/multiprocess_render/src/video_women/moreten.mp4',
]


sources=['/home/enas/catkin_ws/src/multiprocess_render/src/video_women/v%d.mp4' %i for i in range(1,47)]
sources2=['/home/enas/catkin_ws/src/multiprocess_render/src/video_women/x%d.mp4' %i for i in range(1,47)]
sources3=['/home/enas/catkin_ws/src/multiprocess_render/src/video_women/y%d.mp4' %i for i in range(1,47)]
sources4=['/home/enas/catkin_ws/src/multiprocess_render/src/video_women/z%d.mp4' %i for i in range(1,47)]

brsources=['/home/enas/catkin_ws/src/multiprocess_render/src/video_women/bridgev%d.mp4' %i for i in range(1,47)]
brsources2=['/home/enas/catkin_ws/src/multiprocess_render/src/video_women/bridgex%d.mp4' %i for i in range(1,47)]
brsources3=['/home/enas/catkin_ws/src/multiprocess_render/src/video_women/bridgey%d.mp4' %i for i in range(1,47)]
brsources4=['/home/enas/catkin_ws/src/multiprocess_render/src/video_women/bridgez%d.mp4' %i for i in range(1,47)]

endbrsources=['/home/enas/catkin_ws/src/multiprocess_render/src/video_women/endbridgev%d.mp4' %i for i in range(1,47)]
endbrsources2=['/home/enas/catkin_ws/src/multiprocess_render/src/video_women/endbridgex%d.mp4' %i for i in range(1,47)]
endbrsources3=['/home/enas/catkin_ws/src/multiprocess_render/src/video_women/endbridgey%d.mp4' %i for i in range(1,47)]
endbrsources4=['/home/enas/catkin_ws/src/multiprocess_render/src/video_women/endbridgez%d.mp4' %i for i in range(1,47)]
class display_answer:
    
    def __init__(self,source):


        self.text_sub = rospy.Subscriber(source, String, self.callback)

        self.q =Queue()
        self.qtime=Queue()
        self.q.put(sources[0])
        self.qtime.put(994)
        self.playvideos()    

 
    def playit(self):
      global index,state

      url= self.q.get()
      print url 
      media=self.instance.media_new(url)
      self.player.set_media(media)
      self.player.set_rate(0.9)
      self.player.play()
      media.release()
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

                    self.q.put(sources2[index]) 

                    self.qtime.put(994)
           elif state=="v":              


                    self.q.put(sources[index]) 

                    self.qtime.put(994)
           elif state=="y":               

                    self.q.put(sources3[index]) 

                    self.qtime.put(994)
           elif state=="z":

                    self.q.put(sources4[index]) 


                    self.qtime.put(994)

  
           if index>39 or index==39:

                index=0
           else:
               index=index+1

           
   
        
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
         worker.start()
         worker.join()





    def callback(self, data):
        global index
        mlist = [int(e) if e.isdigit() else e for e in str(data.data).split(',')]
        print mlist
        if state=="x":
                 
                  self.q.put(brsources2[index])
                  self.qtime.put(994)
                  if mlist[0]==0:  
                    self.q.put(lionfish[0])
                    self.qtime.put(3976)
                  elif mlist[0]==1:  
                    self.q.put(lionfish[1])
                    self.qtime.put(3976)
                  elif mlist[0]==2:  
                    self.q.put(lionfish[2])
                    self.qtime.put(3976)
                  elif mlist[0]==3:  
                    self.q.put(lionfish[3])
                    self.qtime.put(3976)
                  elif mlist[0]==4:  
                    self.q.put(lionfish[4])
                    self.qtime.put(3976)
                  elif mlist[0]==5:  
                    self.q.put(lionfish[5])
                    self.qtime.put(3976)
                  elif mlist[0]==6:  
                    self.q.put(lionfish[6])
                    self.qtime.put(3976)
                  elif mlist[0]==7:  
                    self.q.put(lionfish[7])
                    self.qtime.put(3976)
                  elif mlist[0]==8:  
                    self.q.put(lionfish[8])
                    self.qtime.put(3976)
                  elif mlist[0]==9:  
                    self.q.put(lionfish[9])
                    self.qtime.put(3976)
                  elif mlist[0]==10:  
                    self.q.put(lionfish[10])
                    self.qtime.put(3976)
                  elif mlist[0]>10:  
                    self.q.put(lionfish[11])
                    self.qtime.put(3976)
                  self.q.put(endbrsources2[index+1])
                  self.qtime.put(994)
                  index=index+2
                  if index>39 or index==39:
                      index=0 

        elif state=="v": 
                  self.q.put(brsources[index])
                  self.qtime.put(994)
                  if mlist[0]==0:  
                    self.q.put(lionfish[0])
                    self.qtime.put(3976)
                  elif mlist[0]==1:  
                    self.q.put(lionfish[1])
                    self.qtime.put(3976)
                  elif mlist[0]==2:  
                    self.q.put(lionfish[2])
                    self.qtime.put(3976)
                  elif mlist[0]==3:  
                    self.q.put(lionfish[3])
                    self.qtime.put(3976)
                  elif mlist[0]==4:  
                    self.q.put(lionfish[4])
                    self.qtime.put(3976)
                  elif mlist[0]==5:  
                    self.q.put(lionfish[5])
                    self.qtime.put(3976)
                  elif mlist[0]==6:  
                    self.q.put(lionfish[6])
                    self.qtime.put(3976)
                  elif mlist[0]==7:  
                    self.q.put(lionfish[7])
                    self.qtime.put(3976)
                  elif mlist[0]==8:  
                    self.q.put(lionfish[8])
                    self.qtime.put(3976)
                  elif mlist[0]==9:  
                    self.q.put(lionfish[9])
                    self.qtime.put(3976)
                  elif mlist[0]==10:  
                    self.q.put(lionfish[10])
                    self.qtime.put(3976)
                  elif mlist[0]>10:  
                    self.q.put(lionfish[11])
                    self.qtime.put(3976)
                  self.q.put(endbrsources[index+1])
                  self.qtime.put(994)
                  index=index+2
                  if index>39 or index==39:
                      index=0              
                   
        elif state=="y":
                  self.q.put(brsources3[index])
                  self.qtime.put(994)
                  if mlist[0]==0:  
                    self.q.put(lionfish[0])
                    self.qtime.put(3976)
                  elif mlist[0]==1:  
                    self.q.put(lionfish[1])
                    self.qtime.put(3976)
                  elif mlist[0]==2:  
                    self.q.put(lionfish[2])
                    self.qtime.put(3976)
                  elif mlist[0]==3:  
                    self.q.put(lionfish[3])
                    self.qtime.put(3976)
                  elif mlist[0]==4:  
                    self.q.put(lionfish[4])
                    self.qtime.put(3976)
                  elif mlist[0]==5:  
                    self.q.put(lionfish[5])
                    self.qtime.put(3976)
                  elif mlist[0]==6:  
                    self.q.put(lionfish[6])
                    self.qtime.put(3976)
                  elif mlist[0]==7:  
                    self.q.put(lionfish[7])
                    self.qtime.put(3976)
                  elif mlist[0]==8:  
                    self.q.put(lionfish[8])
                    self.qtime.put(3976)
                  elif mlist[0]==9:  
                    self.q.put(lionfish[9])
                    self.qtime.put(3976)
                  elif mlist[0]==10:  
                    self.q.put(lionfish[10])
                    self.qtime.put(3976)
                  elif mlist[0]>10:  
                    self.q.put(lionfish[11])
                    self.qtime.put(3976)
                  self.q.put(endbrsources3[index+1])
                  self.qtime.put(994)
                  index=index+2
                  if index>39 or index==39:
                      index=0 

        elif state=="z":
                  self.q.put(brsources4[index])
                  self.qtime.put(994)
                  if mlist[0]==0:  
                    self.q.put(lionfish[0])
                    self.qtime.put(3976)
                  elif mlist[0]==1:  
                    self.q.put(lionfish[1])
                    self.qtime.put(3976)
                  elif mlist[0]==2:  
                    self.q.put(lionfish[2])
                    self.qtime.put(3976)
                  elif mlist[0]==3:  
                    self.q.put(lionfish[3])
                    self.qtime.put(3976)
                  elif mlist[0]==4:  
                    self.q.put(lionfish[4])
                    self.qtime.put(3976)
                  elif mlist[0]==5:  
                    self.q.put(lionfish[5])
                    self.qtime.put(3976)
                  elif mlist[0]==6:  
                    self.q.put(lionfish[6])
                    self.qtime.put(3976)
                  elif mlist[0]==7:  
                    self.q.put(lionfish[7])
                    self.qtime.put(3976)
                  elif mlist[0]==8:  
                    self.q.put(lionfish[8])
                    self.qtime.put(3976)
                  elif mlist[0]==9:  
                    self.q.put(lionfish[9])
                    self.qtime.put(3976)
                  elif mlist[0]==10:  
                    self.q.put(lionfish[10])
                    self.qtime.put(3976)
                  elif mlist[0]>10:  
                    self.q.put(lionfish[11])
                    self.qtime.put(3976)
                  self.q.put(endbrsources4[index+1])
                  self.qtime.put(994)
                  index=index+2
                  if index>39 or index==39:
                      index=0 
           
          
        print "starting now.........................................."+ str(datetime.datetime.now()) 


def main():
    
    rospy.init_node('display_answer')
   
    arg_defaults = {
        'source': '/render1/text1',
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
