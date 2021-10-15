#!/usr/bin/python

import rospy
from std_msgs.msg import Int32MultiArray
from std_msgs.msg import MultiArrayDimension
from geometry_msgs.msg import Twist

class MotorController:
    def __init__(self):
        self.pub = rospy.Publisher("pca9685/motor_command", Int32MultiArray, queue_size=1000)
        self.sub = rospy.Subscriber("motors/motor_twist", Twist, self.callback)
        self.msg = Int32MultiArray()
        self.msg.layout.dim.append(MultiArrayDimension())
        self.msg.layout.dim[0].label = "pca9685/motor_command"
        self.msg.layout.dim[0].size = 16
        self.msg.layout.dim[0].stride = 16

        self.vel_zero = 4700
        self.dir_zero = 4820

        self.vel_max = 600
        self.dir_max = 2000

        # self.msg.data = [4900, 4900, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

    
    def callback(self, twist):
        if twist.linear.x >= 0:
            x_val = int(self.vel_zero + (twist.linear.x * self.vel_max))
        else:
            x_val = int(self.vel_zero + (twist.linear.x * self.vel_max) + 200)
        z_val = int(self.dir_zero + (twist.angular.z * self.dir_max))
        self.msg.data = [x_val, z_val, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
        self.pub.publish(self.msg)


def main():
    rospy.init_node('motor_driver')
    obc = MotorController()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")


if __name__ == '__main__':
    main()
