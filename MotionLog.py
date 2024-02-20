#!/usr/bin/env python3

import rospy
from tkinter import *
from std_msgs.msg import String
from turtlesim.msg import Pose

class MotionLogNode:
    def __init__(self):
        rospy.init_node("MotionLog")
        
        self.root = Tk()
        self.root.title("Motion Log")
        self.root.geometry("400x400")

        self.text = Text(self.root)
        self.text.pack()

        self.clear_button = Button(self.root, text="Clear", command=self.clear_text)
        self.clear_button.pack()

        self.rate = rospy.Rate(10)  # 10 Hz

    def clear_text(self):
        self.text.delete(1.0, END)

    def log_motion_data(self, data):
        motion_data_str = "Motion Control: {}\n".format(data.data)
        self.text.insert(END, motion_data_str)
        self.text.see(END)

    def log_turtle_position(self, pose):
        turtle_position_str = "Turtle Position: ({:.2f}, {:.2f})\n".format(pose.x, pose.y)
        self.text.insert(END, turtle_position_str)
        self.text.see(END)

    def run(self):
        sub_motion_control = rospy.Subscriber("/motion_control_data", String, callback=self.log_motion_data)
        sub_turtle_position = rospy.Subscriber("/turtle1/pose", Pose, callback=self.log_turtle_position)
        self.root.mainloop()

if __name__ == "__main__":
    node = MotionLogNode()
    node.run()

