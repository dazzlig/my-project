#!/usr/bin/env python3
import rospy
from std_msgs.msg import String



rospy.init_node('talker', anonymous=True)
pub = rospy.Publisher('/chatter', String, queue_size=10)
rate = rospy.Rate(1)  # 1 Hz

while not rospy.is_shutdown():
    hello_str = "12가3456"
    pub.publish(hello_str)
    rate.sleep()

