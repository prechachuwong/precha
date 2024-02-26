#!/usr/bin/env python3
from tkinter import *
import rospy
from geometry_msgs.msg import Twist
from std_srvs.srv import Empty
from turtlesim.msg import Pose
import math

rospy.init_node("GUI_Remote")

frame = Tk()
frame.title("REMOTE")
frame.geometry("400x400")

pub = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size=10)
stop_code_flag = False

def move_linear(velocity):
    cmd = Twist()
    cmd.linear.x = velocity
    cmd.angular.z = 0.0
    pub.publish(cmd)

def move_angular(angular_velocity):
    cmd = Twist()
    cmd.linear.x = 0.0
    cmd.angular.z = angular_velocity
    pub.publish(cmd)

def move_diagonal_linear(velocity, angle_degrees):
    angle_radians = math.radians(angle_degrees)
    cmd = Twist()
    cmd.linear.x = velocity
    cmd.linear.y = velocity * math.tan(angle_radians)
    cmd.angular.z = 0.0
    pub.publish(cmd)

def forward():
    move_linear(1.0)

def backward():
    move_linear(-1.0)

def left():
    move_angular(1.0)

def right():
    move_angular(-1.0)

def forward_left():
    move_diagonal_linear(1.0, 45)

def forward_right():
    move_diagonal_linear(1.0, -45)

def backward_left():
    move_diagonal_linear(-1.0, 45)

def backward_right():
    move_diagonal_linear(-1.0, -45)

def stop():
    move_linear(0.0)

def reset_turtle():
    rospy.wait_for_service("/reset")
    reset_proxy = rospy.ServiceProxy("/reset", Empty)
    reset_proxy()

def run(pose):
    global stop_code_flag
    if not stop_code_flag:
        if pose.x > 9.0 or pose.x < 2.0 or pose.y > 9.0 or pose.y < 2.0:
            cmd = Twist()
            cmd.linear.x = 0.5
            cmd.angular.z = 0.5
            pub.publish(cmd)
        else:
            cmd = Twist()
            cmd.linear.x = 2.0
            cmd.angular.z = 0.0
            pub.publish(cmd)

def start():
    global stop_code_flag
    stop_code_flag = False
    rate = rospy.Rate(10)  # 10 Hz
    pub = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size=10)
    sub = rospy.Subscriber("/turtle1/pose", Pose, callback=run)
    while not stop_code_flag:
        rate.sleep()

def stop_code():
    global stop_code_flag
    stop_code_flag = True

button_style = {"font": ("Arial", 14), "width": 10, "height": 2}

B1 = Button(text="Forward", command=forward, **button_style)
B1.place(x=120, y=20)

B2 = Button(text="Backward", command=backward, **button_style)
B2.place(x=120, y=220)

B3 = Button(text="Turn Left", command=left, **button_style)
B3.place(x=20, y=120)

B4 = Button(text="Turn Right", command=right, **button_style)
B4.place(x=220, y=120)

#B5 = Button(text="Forward Left", command=forward_left, **button_style)
#B5.place(x=40, y=40)

#B6 = Button(text="Forward Right", command=forward_right, **button_style)
#B6.place(x=200, y=40)

#B7 = Button(text="Backward Left", command=backward_left, **button_style)
#B7.place(x=40, y=200)

#B8 = Button(text="Backward Right", command=backward_right, **button_style)
#B8.place(x=200, y=200)

#B_stop = Button(text="Stop", command=stop, **button_style)
#B_stop.place(x=140, y=120)

#B_reset = Button(text="Reset Turtle", command=reset_turtle, **button_style)
#B_reset.place(x=140, y=300)

#B_run = Button(text="Run Code", command=start, **button_style)
#B_run.place(x=140, y=350)

#B_stop_code = Button(text="Stop Code", command=stop_code, **button_style)
#B_stop_code.place(x=140, y=400)

frame.mainloop()




