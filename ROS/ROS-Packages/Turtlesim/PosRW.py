#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

###############################################################################

def velocity_sender():
        speed = int(input("Input your speed:"))
        distance_target = int (input("Type your distance:"))
        direction= input("Type your direction:")
        velocity_msg.angular.x=0
        velocity_msg.angular.y=0
        velocity_msg.angular.z=0
        velocity_msg.linear.x=0
        velocity_msg.linear.y=0
        velocity_msg.linear.z=0

        if direction=='x':
            velocity_msg.linear.x=speed
        elif direction=='y':
            velocity_msg.linear.y=speed
        elif direction=='z':
            velocity_msg.linear.z=speed

        t0= rospy.Time.now().to_sec()
        distance_moved=0

        while(distance_moved<distance_target):
            velocity_send.publish(velocity_msg)
            t1=rospy.Time.now().to_sec()
            distance_moved= abs(speed)*(t1-t0)

        velocity_msg.linear.x=0
        velocity_msg.linear.y=0
        velocity_msg.linear.z=0
        velocity_send.publish(velocity_msg)


###############################################################################

'''
The ROS python library runs additional threads to handle message subscription and publishing.
So when you call rospy.Subscribe in your code, it doesn't check for incoming messages and
execute callbacks itself. It simply adds the topic and function to a list.
This list is regularly checked in a different thread which executes the callbacks as needed.
This is why you don't need any polling in your code to make the message callbacks work and you need to add your looping code in it.
'''

def pos_recieve_action(message):
    rospy.loginfo("recieved({})".format(message))
    velocity_sender()

###############################################################################

rospy.init_node('PosRW',anonymous=True)
velocity_send=rospy.Publisher('/turtle1/cmd_vel',Twist,queue_size=10)
velocity_msg= Twist()

rospy.Subscriber('/turtle1/pose',Pose,pos_recieve_action)
rospy.spin()
