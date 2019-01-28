#!/usr/bin/env python


from std_msgs.msg import String
import rospy
import sys
from PyQt4 import QtGui
import datetime
import time

class user_output_text:

    
    def __init__(self,source,sink):
      
        self.text_sub = rospy.Subscriber(source, String, self.callback)
        self.text_pub = rospy.Publisher(sink, String, queue_size=10, latch=True)
        self.initUI()
        
        
        
    def initUI(self):      
        self.app = QtGui.QApplication([])
        self.win = QtGui.QWidget()
        self.win.setStyleSheet("background-color:black; color:white; font-family:'Times New Roman';")

        self.win.label = QtGui.QLabel("Ask a question", self.win)
        self.win.label.move(50, 50)
        self.win.label.setFixedWidth(800)
        self.win.label.setFixedHeight(100)
        self.win.label.setWordWrap(True)

        self.win.label2 = QtGui.QLabel("Status", self.win)
        self.win.label2.move(50, 150)
        self.win.label2.setFixedWidth(800)


        #self.win.le = QtGui.QLineEdit(self.win)
        #self.win.le.setFixedWidth(300)
        #self.win.le.move(150, 50)
        self.win.label.setStyleSheet("font-size:25px")
        self.win.label2.setStyleSheet("font-size:30px;color:red")
        self.win.setGeometry(700, 300, 850, 250)
        self.win.setWindowTitle('Answer')
        self.win.show()
        self.app.exec_()

        

        
   
    def callback(self, data):  
           f= open("/home/enas/text.txt","a")
           now = datetime.datetime.now() 
           f.write(now.strftime("response text output-%H:%M:%S"))
           f.close()
           self.win.label.setText(data.data)
           self.win.label2.setText(" Next Question")
           self.text_pub.publish("next") 
           time.sleep(1)
           self.win.label2.setText("Status")    


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
