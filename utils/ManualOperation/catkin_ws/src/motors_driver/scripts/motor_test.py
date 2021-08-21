#!/usr/bin/python

"""
Class for low level control of owr car. It assumes ros-12cpwmboard has been
installed
"""
import rospy
from std_msgs.msg import Int32MultiArray
from std_msgs.msg import MultiArrayDimension

# class MotorController:
#     def __init__():
#         self.node

def talker():
    rospy.init_node('motor_test')
    
    pub = rospy.Publisher('command', Int32MultiArray, queue_size=1000)
    rate = rospy.Rate(0.5) # 10hz
    
    msg = Int32MultiArray()
    print(msg)
    msg.layout.dim.append(MultiArrayDimension())
    msg.layout.dim[0].label = "command"
    msg.layout.dim[0].size = 16
    msg.layout.dim[0].stride = 16
    
    val90 = [4900, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
    val20 = [2900, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
    val180 = [6900, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
    
    velocity0 = [-1, 4900, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
    velocityF = [-1, 2900, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
    velocityB = [-1, 6900, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
    
#     msg.data = [6900, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
    
    counter = 0
    while not rospy.is_shutdown():
#         hello_str = "hello world %s" % rospy.get_time()
        
        if counter == 0:
            msg.data = val90
        elif counter == 1:
            msg.data = val20
        elif counter == 2:
            msg.data = val180
            
#         if counter == 0:
#             msg.data = velocity0
#         elif counter == 1:
#             msg.data = velocityF
#         elif counter == 2:
#             msg.data = velocity0
            
        rospy.loginfo("sending")
        print("{}".format(counter))
        pub.publish(msg)
        rate.sleep()
        counter += 1
        counter = counter % 3

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
