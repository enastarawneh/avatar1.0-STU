#!/usr/bin/env python


from std_msgs.msg import String
import rospy
import sys
from PyQt4 import QtGui
from cv_bridge import CvBridge, CvBridgeError;
import unicodedata
import datetime
recording=True


class user_input:

    
    def __init__(self,sink):
      
        self.text_pub = rospy.Publisher(sink, String, queue_size=10, latch=True)
       
        self.initUI()
        
        
        
    def initUI(self):      
        self.app = QtGui.QApplication([])
        self.win = QtGui.QWidget()
        self.win.setStyleSheet("background-color:black; color:white")
        

        self.win.btn1 = QtGui.QPushButton('Ask ', self.win)   
        self.win.btn1.move(50, 100)
        self.win.btn1.setStyleSheet("background-color:#871202")
        self.win.btn1.clicked.connect(self.readtext  )
   


        self.win.label = QtGui.QLabel("Question:", self.win) 
        self.win.label.move(50, 50)
       
        self.win.le = QtGui.QLineEdit(self.win)
        self.win.le.setFixedWidth(300)
        self.win.le.move(130, 50)
        self.win.le.textChanged.connect(self.record)
        
        self.win.setGeometry(200, 300, 450, 150)
        self.win.setWindowTitle('Ask a Question')
        self.win.show()
        self.app.exec_()

        

        
   
    def readtext(self):
           global recording
           
           f= open("/home/enas/text.txt","a")
           now = datetime.datetime.now()  
           f.write(now.strftime("text submitted-%H:%M:%S, "))
           f.close() 
           self.text2=str(self.win.le.text())
           self.text_pub.publish(str(self.text2))
           recording=True

    def record(self):
           global recording

           if recording==True:
            recording=False
            f= open("/home/enas/text.txt","a")
            now = datetime.datetime.now() 
            f.write("\n"+now.strftime("text entered-%H:%M:%S, "))
            f.close()
              

def main():
    
    rospy.init_node('user_input')
    
  
    
    arg_defaults = {
        'sink': '/render1/text1'
   
        }
    args = updateArgs(arg_defaults)
    user_input(**args)
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
