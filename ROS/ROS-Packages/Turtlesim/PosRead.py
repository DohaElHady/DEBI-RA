#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist

def pos_recieve_action(message):
    rospy.loginfo("recieved({})".format(message))

rospy.init_node('pos_recieve',anonymous=True)
rospy.Subscriber('/turtle1/cmd_vel',Twist,pos_recieve_action)
rospy.spin()
