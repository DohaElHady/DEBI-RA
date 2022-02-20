#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist


rospy.init_node('velocity_teller',anonymous=True)
velocity_send=rospy.Publisher('/turtle1/cmd_vel',Twist,queue_size=10)
rate=rospy.Rate(10)
velocity_msg= Twist()

while not rospy.is_shutdown():
  
    speed = int(input("Input your speed:"))
    distance_target = int (input("Type your distance:"))

    velocity_msg.linear.x=speed
    velocity_msg.linear.y=0
    velocity_msg.linear.z=0
    velocity_msg.angular.x=0
    velocity_msg.angular.y=0
    velocity_msg.angular.z=0

    t0= rospy.Time.now().to_sec()
    distance_moved=0

    while(distance_moved<distance_target):
        velocity_send.publish(velocity_msg)
        t1=rospy.Time.now().to_sec()
        distance_moved= abs(speed)*(t1-t0)

    velocity_msg.linear.x=0
    velocity_send.publish(velocity_msg)
    rate.sleep()
