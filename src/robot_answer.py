#!/usr/bin/env python


from std_msgs.msg import String
import rospy
import sys
import pathos.multiprocessing as mp
#from multiprocessing import Pool
import subprocess
import os
#from bgl import platform

newindex=0


class robot_answer:

    
    def __init__(self, source1, source2):
        global newindex
        self.text_sub = rospy.Subscriber(source1, String, self.callback)
        self.text_sub2 = rospy.Subscriber(source2, String, self.callback2)      
       
        pool = mp.ProcessingPool(6)
        pool.map(self.multi_run_wrapper, [(0,newindex,(newindex+8)),(1,(newindex+4),(newindex+15)),(2,(newindex+11),(newindex+26)),(3,(newindex+22),(newindex+36)),(4,(newindex+32),(newindex+51)),(5,(newindex+47),(newindex+72))])


    def multi_run_wrapper(self, args):
                
               return self.my_function(*args) 
               
              

    def my_function(self, x,var2, var3):
         #vdisplay = Xvfb()
         #vdisplay.start()
         p = subprocess.Popen(["vglrun xvfb-run --auto-servernum --server-args='-screen 0 1280x1024x24:32' blender  /home/enas/blender-files/arab-guy/lipsynctarab"+str(x)+".blend --python /home/enas/catkin_ws/src/multiprocess_render/src/scripts/try"+str(x)+".py -- "+str(var2)+" "+str(var3)], shell=True)    
         #os.system("xvfb-run --auto-servernum --server-args='-screen 0 1280x1024x24:32' blender  /home/enas/blender-files/arab-guy/lipsynctarab"+str(x)+".blend --python /home/enas/catkin_ws/src/multiprocess_render/src/scripts/try"+str(x)+".py -- "+str(var2)+" "+str(var3)) 
              


         #vdisplay.stop()          
        
             
        
    def callback(self, data):
       gotit=True  
       #newindex=((index+20)%25)*24
       

       


    def callback2(self, data):
        gotit=True
          #global index, state
          #mList = [int(e) if e.isdigit() else e for e in str(data.data).split(',')]
          #index=mList[0]
          #state=mList[1]


def main():
   
    rospy.init_node('robot_answer')
   
    arg_defaults = {
        'source1': '/render1/text2',
        'source2': '/render1/index'
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
            print ("We have args " + val + " value " + args[name])
    return(args)


if __name__ == '__main__':
    main()
