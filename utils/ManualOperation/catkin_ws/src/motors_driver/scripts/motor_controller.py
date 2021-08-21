#!/usr/bin/python

import rospy
from std_msgs.msg import Int32MultiArray
from std_msgs.msg import MultiArrayDimension
from geometry_msgs.msg import Twist

class MotorController:
    def __init__(self):
        self.pub = rospy.Publisher('command', Int32MultiArray, queue_size=1000)
        self.sub = rospy.Subscriber("motors/motor_twist", Twist, self.callback)
        self.msg = Int32MultiArray()
        self.msg.layout.dim.append(MultiArrayDimension())
        self.msg.layout.dim[0].label = "command"
        self.msg.layout.dim[0].size = 16
        self.msg.layout.dim[0].stride = 16

        self.vel_zero = 4900
        self.dir_zero = 4500

        self.vel_max = 300
        self.dir_max = 2000

        # self.msg.data = [4900, 4900, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

    
    def callback(self, twist):
        if twist.linear.x >= 0:
            x_val = int(self.vel_zero + (twist.linear.x * self.vel_max))
        else:
            x_val = int(self.vel_zero + (twist.linear.x * self.vel_max) - 200)
        z_val = int(self.dir_zero + (twist.angular.z * self.dir_max))
        self.msg.data = [x_val, z_val, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

        # print(twist.linear.x)
        print(twist.angular.z)
        print(self.msg.data)
        self.pub.publish(self.msg)


def main():
    rospy.init_node('motor_controller')
    obc = MotorController()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")


if __name__ == '__main__':
    main()

# def talker():
    
#     pub = rospy.Publisher('command', Int32MultiArray, queue_size=1000)
#     rate = rospy.Rate(0.5) # 10hz
    
#     msg = Int32MultiArray()
#     print(msg)
#     msg.layout.dim.append(MultiArrayDimension())
#     msg.layout.dim[0].label = "command"
#     msg.layout.dim[0].size = 16
#     msg.layout.dim[0].stride = 16
    
#     val90 = [4900, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
#     val20 = [2900, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
#     val180 = [6900, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
    
#     velocity0 = [-1, 4900, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
#     velocityF = [-1, 2900, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
#     velocityB = [-1, 6900, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
    
# #     msg.data = [6900, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
    
#     counter = 0
#     while not rospy.is_shutdown():
# #         hello_str = "hello world %s" % rospy.get_time()
        
#         if counter == 0:
#             msg.data = val90
#         elif counter == 1:
#             msg.data = val20
#         elif counter == 2:
#             msg.data = val180
            
# #         if counter == 0:
# #             msg.data = velocity0
# #         elif counter == 1:
# #             msg.data = velocityF
# #         elif counter == 2:
# #             msg.data = velocity0
            
#         rospy.loginfo("sending")
#         print("{}".format(counter))
#         pub.publish(msg)
#         rate.sleep()
#         counter += 1
#         counter = counter % 3
