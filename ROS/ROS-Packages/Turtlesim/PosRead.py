#!/usr/bin/env python3
import rospy
from turtlesim.msg import Pose

def pos_recieve_action(message):
    rospy.loginfo("recieved({})".format(message))

rospy.init_node('pos_recieve',anonymous=True)
rospy.Subscriber('/turtle1/pose',Pose,pos_recieve_action)
rospy.spin()
