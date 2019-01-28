#!/usr/bin/env python

from geometry_msgs.msg import Twist
from std_msgs.msg import String
import rospy
import sys
import os
import vlc
from Queue import Queue
from threading import Thread,Timer
#import time
from pygame import time
from random import randint
import datetime
avatar="male"
emotion="normal"
idle=True
state="v"
index=0
newone=False
camein=[False,False,False,False,False,False]
path=['/home/enas/catkin_ws/src/multiprocess_render/src/video/yes%d.mp4' %i for i in range(1,7)]
 
segtime=[998,998,998,998,998,998]
countdown=17
happywomensources=[]
happywomensources2=[]
happywomensources3=[]
happywomensources4=[]

womensources=[]
womensources2=[]
womensources3=[]
womensources4=[]

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
    
    def __init__(self,source,source1,source2,source3,source4,source5,source6,source0, sink, sink2,source7,source8 ):

        self.text_pub = rospy.Publisher(sink, String, queue_size=10, latch=True)
        self.text_sub = rospy.Subscriber(source, String, self.callback)
        self.text_sub1 = rospy.Subscriber(source1, String, self.callback1)
        self.text_sub2 = rospy.Subscriber(source2, String, self.callback2)
        self.text_sub3 = rospy.Subscriber(source3, String, self.callback3)
        self.text_sub4 = rospy.Subscriber(source4, String, self.callback4)
        self.text_sub5 = rospy.Subscriber(source5, String, self.callback5)
        self.text_sub6 = rospy.Subscriber(source6, String, self.callback6)
        self.text_sub8 = rospy.Subscriber(source7, String, self.callback7)
        self.text_sub9 = rospy.Subscriber(source8, String, self.callback8)
        self.text_sub7=rospy.Subscriber(source0,Twist,self.callback0)
        self.text_pub2 = rospy.Publisher(sink2, String, queue_size=10, latch=True)
        self.q =Queue()
        self.qtime=Queue()
        self.q.put(sources[0])
        self.qtime.put(998)
        self.playvideos()    

 
    def playit(self):
      global index,state, newone, countdown, camein, path, segtime, avatar,emotion,idle

      url= self.q.get()
      print url
      media=self.instance.media_new(url)
      self.player.set_media(media)
      self.player.set_rate(0.9)
      print self.player.get_rate()
      self.player.play()
      media.release()

      
      time.delay(self.qtime.get())
     

      if self.q.empty():
           if not newone:   
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
           if newone and countdown==0:
             print camein[0]
             if camein[0]==True:
              self.q.put(path[0])
              self.qtime.put(segtime[0])
             if camein[1]==True:
              self.q.put(path[1])
              self.qtime.put(segtime[1])
             if camein[2]==True:
              self.q.put(path[2])
              self.qtime.put(segtime[2])
             if camein[3]==True:
              self.q.put(path[3])
              self.qtime.put(segtime[3])
             if camein[4]==True:
              self.q.put(path[4])
              self.qtime.put(segtime[4])
             if camein[5]==True:
              self.q.put(path[5])
              self.qtime.put(segtime[5])
             self.text_pub2.publish("hello")
             newone=False 
             print str(segtime[0]+segtime[1]+segtime[2]+segtime[3]+segtime[4]+segtime[5])
             index=index+2
             

           if state=="x":
               
                  if avatar=="male":
                    if idle==True:
                      self.q.put(sources2[index])
                    else:
                      self.q.put(ensources2[index]) 
                  else:
                    if emotion=="happy":
                      self.q.put(happywomensources2[index])
                    else:
                      self.q.put(womensources2[index])
                  self.qtime.put(998)
           elif state=="v":              

                   if avatar=="male":
                    if idle==True:
                      self.q.put(sources[index])
                    else:
                      self.q.put(ensources[index]) 
                   else:
                    if emotion=="happy":
                      self.q.put(happywomensources[index])
                    else:
                      self.q.put(womensources[index])

                   self.qtime.put(998)
           elif state=="y":               
                  if avatar=="male":
                    if idle==True:
                      self.q.put(sources3[index])
                    else:
                      self.q.put(ensources3[index]) 
                  else:
                    if emotion=="happy":
                      self.q.put(happywomensources3[index])
                    else:
                      self.q.put(womensources3[index])


                  self.qtime.put(998)
           elif state=="z":
               
                  if avatar=="male":
                    if idle==True:
                      self.q.put(sources4[index])
                    else:
                      self.q.put(ensources4[index]) 
                  else:
                    if emotion=="happy":
                      self.q.put(happywomensources4[index])
                    else:
                      self.q.put(womensources4[index])


                  self.qtime.put(998)
           print "this is the index:"+str(index)
  
           if index>39 or index==39:

                index=0
           else:
               index=index+1
           if newone:
               countdown=countdown-1
               print "this is the countdown"+ str(countdown) 
           self.text_pub.publish(str(index)+","+state)

   
        
    def playvideos(self): 
      global index
      self.instance = vlc.Instance('--input-repeat=-1', '--fullscreen', '--mouse-hide-timeout=0')
      self.player=self.instance.media_player_new()

      index=1


      while not self.q.empty():

         worker = Thread(target=self.playit)
         worker.setDaemon(True)
         worker.start()
         worker.join()
 


    def callback1(self, data):
        global camein, segtime, path 
        mList = [int(e) if e.isdigit() else e for e in str(data.data).split(',')]
        #self.q.put(mList[0])
        path[0]=mList[0]
        camein[0]=True
        segtime[0]=int((float(mList[3]-mList[2])/24)*994)
        print str(segtime[0])  
        #self.qtime.put(int((float(mList[3]-mList[2]+1)/24)*998))
       
        f= open("/home/enas/text.txt","a")
        now = datetime.datetime.now() 
        f.write(now.strftime("1 is done -%H:%M:%S"))
        f.close()

    def callback2(self, data):
        global camein, segtime, path 
        mList = [int(e) if e.isdigit() else e for e in str(data.data).split(',')]
        #self.q.put(mList[0])
        path[1]=mList[0]
        camein[1]=True
        segtime[1]=int((float(mList[3]-mList[2])/24)*994)
        print str(segtime[1])
        #self.qtime.put(int((float(mList[3]-mList[2]+1)/24)*998))
       
        f= open("/home/enas/text.txt","a")
        now = datetime.datetime.now() 
        f.write(now.strftime("2 is done -%H:%M:%S"))
        f.close()

    def callback3(self, data):
        global camein, segtime, path 
        mList = [int(e) if e.isdigit() else e for e in str(data.data).split(',')]
        #self.q.put(mList[0])
        path[2]=mList[0]
        camein[2]=True
        segtime[2]=int((float(mList[3]-mList[2])/24)*994)
        print str(segtime[2])
        #self.qtime.put(int((float(mList[3]-mList[2]+1)/24)*998))
       
        f= open("/home/enas/text.txt","a")
        now = datetime.datetime.now() 
        f.write(now.strftime("3 is done -%H:%M:%S"))
        f.close()

    def callback4(self, data):
        global camein, segtime, path 
        mList = [int(e) if e.isdigit() else e for e in str(data.data).split(',')]
        #self.q.put(mList[0])
        path[3]=mList[0]
        camein[3]=True
        segtime[3]=int((float(mList[3]-mList[2])/24)*994)
        print str(segtime[3])
        #self.qtime.put(int((float(mList[3]-mList[2]+1)/24)*998))
       
        f= open("/home/enas/text.txt","a")
        now = datetime.datetime.now() 
        f.write(now.strftime("4 is done -%H:%M:%S"))
        f.close()

    def callback5(self, data):
        global camein, segtime, path 
        mList = [int(e) if e.isdigit() else e for e in str(data.data).split(',')]
        #self.q.put(mList[0])
        path[4]=mList[0]
        camein[4]=True
        segtime[4]=int((float(mList[3]-mList[2])/24)*994)
        print str(segtime[4])
        #self.qtime.put(int((float(mList[3]-mList[2]+1)/24)*998))
       
        f= open("/home/enas/text.txt","a")
        now = datetime.datetime.now() 
        f.write(now.strftime("5 is done -%H:%M:%S"))
        f.close()

    def callback6(self, data):
        global camein, segtime, path 
        mList = [int(e) if e.isdigit() else e for e in str(data.data).split(',')]
        #self.q.put(mList[0])
        path[5]=mList[0]
        camein[5]=True
        segtime[5]=int((float(mList[3]-mList[2])/24)*994)
        print str(segtime[5]) 
        #self.qtime.put(int((float(mList[3]-mList[2]+1)/24)*998))

       
        f= open("/home/enas/text.txt","a")
        now = datetime.datetime.now() 
        f.write(now.strftime("6 is done -%H:%M:%S"))
        f.close()

    def callback(self, data):
        global newone,countdown,index,idle
        newone= True
        countdown=17
        idle=False
        if state=="x":
                  self.q.put(brsources2[index])
                  self.qtime.put(998)
                  self.q.put(umsources2[(index+1)*2])
                  self.qtime.put(1984)
                  self.q.put(ahsources2[((index+1)*2)+2])
                  self.qtime.put(1984)
                  self.q.put(ahsources2[((index+1)*2)+4])
                  self.qtime.put(1984)
                  index=index+4
                  if index>39 or index==39:
                      index=0 

        elif state=="v":              
                   self.q.put(brsources[index])
                   self.qtime.put(998)
                   self.q.put(umsources[(index+1)*2])
                   self.qtime.put(1984)
                   self.q.put(ahsources[((index+1)*2)+2])
                   self.qtime.put(1984)
                   self.q.put(ahsources[((index+1)*2)+4])
                   self.qtime.put(1984)
                   index=index+4
                   if index>39 or index==39:
                      index=0 

        elif state=="y":
                   self.q.put(brsources3[index])
                   self.qtime.put(998)               
                   self.q.put(umsources3[(index+1)*2])
                   self.qtime.put(1984)
                   self.q.put(ahsources3[((index+1)*2)+2])
                   self.qtime.put(1984)
                   self.q.put(ahsources3[((index+1)*2)+4])
                   self.qtime.put(1984)
                   index=index+4
                   if index>39 or index==39:
                      index=0  

        elif state=="z":
                   self.q.put(brsources2[index])
                   self.qtime.put(998)               
                   self.q.put(umsources4[(index+1)*2])
                   self.qtime.put(1980)
                   self.q.put(ahsources4[((index+1)*2)+2])
                   self.qtime.put(1980)
                   self.q.put(ahsources4[((index+1)*2)+4])
                   self.qtime.put(1984)
                   index=index+4
                   if index>39 or index==39:
                      index=0 
             
        countdown=countdown-7

    def callback0(self, data):
         
         if data.angular.z == -0.5:
            print "hello"
    def callback7(self, data):
         global avatar
         avatar=str(data.data)

    def callback8(self, data):
        global emotion
        emotion=str(data.data)
         


def main():
    
    rospy.init_node('display_answer')
   
    arg_defaults = {
        'sink': '/render1/index',
        'source': '/render1/text1',
        'source1':'/render1/show1',
        'source2':'/render1/show2',
        'source3':'/render1/show3',
        'source4':'/render1/show4',
        'source5':'/render1/show5',
        'source6':'/render1/show6',
        'source0':'/turtle1/cmd_vel',
        'source7':'/display/avatar', 
        'source8':'/display/emotion',   
        'sink2':'/question/next'    
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
