#!/usr/bin/env python


from std_msgs.msg import String
import rospy
import sys
import urllib2
import unicodedata
from urllib2 import HTTPError
import datetime

class wolfram:

    
    def __init__(self,sink,source):
      
        self.text_pub = rospy.Publisher(sink, String, queue_size=10, latch=True)
        self.text_sub = rospy.Subscriber(source, String, self.callback)
       
        
        
        
    def callback(self, data):     
         f= open("/home/enas/text.txt","a")
         now = datetime.datetime.now()  
         f.write(now.strftime("sent to wolfram-%H:%M:%S, "))
         f.close() 
         text2=data.data.encode('utf-8')
         text3=text2.replace(" ","+")
         try:
          content = urllib2.urlopen("https://api.wolframalpha.com/v1/spoken?i="+text3+"%3F&appid=VRE3G5-PXJG5RQER6").read()
         except urllib2.HTTPError:
               content="can you please repeat that question "
               f= open("/home/enas/errorlog.txt","a")
               now = datetime.datetime.now() 
               f.write(now.strftime("wolfram error-%H:%M:%S \n  "))
               f.close()

         f= open("/home/enas/text.txt","a")
         now = datetime.datetime.now()  
         f.write(now.strftime("wolfram response-%H:%M:%S, "))
         f.close() 

         self.text_pub.publish(str(content))
         print "wolfram done" 
       

    
   
def main():
    
    rospy.init_node('wolfram')
    
  
    
    arg_defaults = {
        'sink': '/answer1/text1',
        'source': '/render1/text1' 
        }
    args = updateArgs(arg_defaults)
    wolfram(**args)
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
