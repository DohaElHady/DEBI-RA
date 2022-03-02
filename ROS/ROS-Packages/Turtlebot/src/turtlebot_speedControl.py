#!/usr/bin/env python3
import time
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Imu
from math import *

def euler_from_quaternion(x, y, z, w):
        """
        Convert a quaternion into euler angles (roll, pitch, yaw)
        roll is rotation around x in radians (counterclockwise)
        pitch is rotation around y in radians (counterclockwise)
        yaw is rotation around z in radians (counterclockwise)
        """
        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        roll_x = atan2(t0, t1)

        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch_y = asin(t2)

        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw_z = atan2(t3, t4)
        yaw_z=degree_from_radian(yaw_z)
        return yaw_z #in degrees

def degree_from_radian(yaw_z):
    theta_z=0
    if (yaw_z>0):
        theta_z=(yaw_z/pi)*180
    elif(yaw_z<0):
        theta_z=360-((abs(yaw_z)/pi)*180)
    elif(yaw_z==0):
        theta_z=0
    return theta_z

"""
Intializing Publisher Node
"""
rospy.init_node('velocity_teller',anonymous=True)
velocity_send=rospy.Publisher('cmd_vel',Twist,queue_size=10)
rate=rospy.Rate(10)
global velocity_msg
velocity_msg= Twist()
global angularPose
currentAngle=0
global posZ,pozX,posY,posW,angleZ

"""
Intializing Subscriber Node & Function
"""
def pos_recieve_action(message):
    global posZ,posX,posY,posW
    posX=message.orientation.x
    posY=message.orientation.y
    posZ=message.orientation.z
    posW=message.orientation.w

rospy.Subscriber('/imu',Imu,pos_recieve_action)

"""
Twist msg fast modification:
    In turtlebot it only has linear speed in x direction and angular speed in z direction
"""
def setVelMsg(linX,angZ):
    velocity_msg.angular.z=angZ
    velocity_msg.linear.x=linX
    velocity_msg.angular.x=0
    velocity_msg.angular.y=0
    velocity_msg.linear.y=0
    velocity_msg.linear.z=0

"""
Rotation Function
"""
def rotate(targetAngle):
    global currentAngle
    finalZ=euler_from_quaternion(posX, posY, posZ, posW)
    print(finalZ)

    if targetAngle<currentAngle:
        setVelMsg(0,-1.5)
        while finalZ>targetAngle+0.1:
            velocity_send.publish(velocity_msg)
            finalZ=euler_from_quaternion(posX, posY, posZ, posW)

    elif targetAngle>currentAngle:
        setVelMsg(0,1.5)
        while finalZ<targetAngle+0.1:
            velocity_send.publish(velocity_msg)
            finalZ=euler_from_quaternion(posX, posY, posZ, posW)

    setVelMsg(0,0)
    velocity_send.publish(velocity_msg)
    currentAngle=finalZ
    print(finalZ)


"""
The Main Loop
"""
while not rospy.is_shutdown():
    speed = float(input("Input your speed (max 0.26):"))
    distance_target = int (input("Type your distance:"))
    direction= input("Type your direction (x,-x,y,-y):")
    setVelMsg(0,0)

    if direction=='x':
        rotate(0)
        setVelMsg(abs(speed),0)
    elif direction=='-x':
        rotate(180)
        setVelMsg(abs(speed),0)
    elif direction=='y':
        rotate(90)
        setVelMsg(abs(speed),0)
    elif direction=='-y':
        rotate(270)
        setVelMsg(abs(speed),0)


    t0= rospy.Time.now().to_sec()
    distance_moved=0

    while(distance_moved<distance_target):
        velocity_send.publish(velocity_msg)
        t1=rospy.Time.now().to_sec()
        distance_moved= abs(speed)*(t1-t0)


    setVelMsg(0,0)
    velocity_send.publish(velocity_msg)
    rate.sleep()

