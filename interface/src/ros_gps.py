#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import PointStamped
import random

def talker():
    pub = rospy.Publisher('/gps_chatter', PointStamped, queue_size=10)
    rospy.init_node('gps_talker', anonymous=True)
    rate = rospy.Rate(1)  # 1 Hz

    while not rospy.is_shutdown():
        # 예제 GPS 데이터 생성 (임의의 값으로 대체)
        gps_msg = PointStamped()
        gps_msg.point.x = random.uniform(-90.0, 90.0)  # 위도
        gps_msg.point.y = random.uniform(-180.0, 180.0)  # 경도

        rospy.loginfo(f"Publishing GPS data: {gps_msg.point.x}, {gps_msg.point.y}")
        pub.publish(gps_msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass

