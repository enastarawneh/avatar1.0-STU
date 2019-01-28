
import bpy
from bpy import context
from bpy import data
from bpy import props
from bpy import types
import os
import sys
import subprocess
import shlex
import datetime
oldone="start"


def fix_context():
    """Fix bpy.context if some command (like .blend import) changed/emptied it"""
    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == 'VIEW_3D':
                for region in area.regions:
                    if region.type == 'WINDOW':
                        override = {'window': window, 'screen': screen, 'area': area, 'region': region}
                        bpy.ops.screen.screen_full_area(override)
                        break


 
#proc = subprocess.Popen(["rostopic echo /render1/text1/data"], stdout=subprocess.PIPE, shell=True)

#output = proc.stdout.readline().decode
  
def get_next_speech(): 
  process = subprocess.Popen(shlex.split("rostopic echo /render1/text2/data"), stdout=subprocess.PIPE)
  output = process.stdout.readline()
  output=output.strip()
  output=output.decode()
  process.stdout.close
   
  f= open("/home/enas/text.txt","a")
  now = datetime.datetime.now() 
  f.write(now.strftime("5 got text-%H:%M:%S, "))
  f.close()
  process2 = subprocess.Popen(shlex.split("rostopic echo /render1/index/data"), stdout=subprocess.PIPE)
  output2 = process2.stdout.readline()
  output2=output2.strip()
  output2=output2.decode()
  output2=output2.replace('"','')
  process2.stdout.close


  f= open("/home/enas/text.txt","a")
  now = datetime.datetime.now() 
  f.write(now.strftime("5 got index-%H:%M:%S,  "))
  f.close()

  mList = [int(e) if e.isdigit() else e for e in output2.split(',')]
  index=mList[0]
  state=mList[1]

  if state=="x":

    bpy.ops.wm.open_mainfile(filepath='/home/enas/blender-files/arab-guy/lipsynctarabv25.blend')           

  elif state=="v":              
          
    bpy.ops.wm.open_mainfile(filepath='/home/enas/blender-files/arab-guy/lipsynctarab5.blend')
  elif state=="y":               

    bpy.ops.wm.open_mainfile(filepath='/home/enas/blender-files/arab-guy/lipsynctarabv35.blend')           

  elif state=="z":
          
    bpy.ops.wm.open_mainfile(filepath='/home/enas/blender-files/arab-guy/lipsynctarabv45.blend')


  argv = sys.argv
  argv = argv[argv.index("--") + 1:]  


  scene = context.scene 
  if not scene.sequence_editor:
    scene.sequence_editor_create()



  fix_context()
  f= open("/home/enas/text.txt","a")
  now = datetime.datetime.now() 
  f.write(now.strftime("5 got fix context-%H:%M:%S,  "))
  f.close()

  x=int(float(argv[0]))
  y=int(float(argv[1]))
  newindex=(index+16)*24

  soundstrip = scene.sequence_editor.sequences.new_sound("say", "/home/enas/catkin_ws/src/multiprocess_render/src/audio/say5.mp3", 2, newindex)


  bpy.data.scenes["Scene"].frame_current=newindex-1
  bpy.data.scenes["Scene"].frame_start=newindex
  bpy.data.scenes["Scene"].frame_end=newindex+bpy.data.scenes["Scene"].sequence_editor.sequences_all["say"].frame_final_duration-5
  bpy.data.scenes["Scene"].quicktalk_script_file="/home/enas/catkin_ws/src/multiprocess_render/src/txtscript/script15.txt"
  bpy.data.scenes["Scene"].quicktalk_dict_file="/home/enas/catkin_ws/src/multiprocess_render/src/txtscript/standard_dictionary5"

               
  bpy.ops.object.quicktalk_guess_dialogue()
  bpy.ops.object.quicktalk_guess_lines()
  bpy.ops.object.quicktalk_guess_words()
  bpy.data.scenes["Scene"].use_frame_drop=True
  bpy.data.scenes["Scene"].use_audio_sync=True
  bpy.data.scenes["Scene"].use_audio_scrub
  #bpy.data.screens["Default"].use_play_sequence_editors=True
  bpy.ops.object.quicktalk_plot_timeline()
  bpy.data.scenes["Scene"].frame_current=bpy.data.scenes["Scene"].sequence_editor.sequences_all["say"].frame_final_duration
  #bpy.ops.pose.transforms_clear()
  #bpy.ops.anim.keyframe_insert()
  bpy.ops.screen.back_to_previous()
  bpy.data.scenes["Scene"].render.filepath="/home/enas/catkin_ws/src/multiprocess_render/src/video/yes6.mp4"#argv[0]
 
  bpy.data.scenes["Scene"].frame_start=newindex+x
  bpy.data.scenes["Scene"].frame_end=newindex+y

  f= open("/home/enas/text.txt","a")
  now = datetime.datetime.now() 
  f.write(now.strftime("5 before render-%H:%M:%S, "))
  f.close()
  bpy.ops.render.opengl(animation=True)

  f= open("/home/enas/text.txt","a")
  now = datetime.datetime.now() 
  f.write(now.strftime("5 render-%H:%M:%S, "))
  f.close()
  subprocess.Popen(shlex.split("rostopic pub /render1/show6 std_msgs/String /home/enas/catkin_ws/src/multiprocess_render/src/video/yes6.mp4,x,"+str(x)+","+str(y)+",/render1/show6"), stdout=subprocess.PIPE)
  process.stdout.close
  #os.system("convert -bordercolor white -border 0 -layers OptimizePlus -delay 4 /home/enas/try/*.png -loop 0 /home/enas/try/test.gif")
  #bpy.ops.screen.animation_play()
  #bpy.ops.wm.redraw_timer(type='ANIM_PLAY',iterations=1)
  #bpy.ops.wm.quit_blender()
  get_next_speech()

# In ROS, nodes are uniquely named. If two nodes with the same
# node are launched, the previous one is kicked off. The
# anonymous=True flag means that rospy will choose a unique
# name for our 'listener' node so that multiple listeners can
# run simultaneously.

get_next_speech()

