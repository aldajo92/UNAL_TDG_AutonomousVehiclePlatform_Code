#!/usr/bin/env python3

import rospy

from geometry_msgs.msg import Point
from geometry_msgs.msg import Twist

class Navigation:

    def __init__(self):

        self.subscriber = rospy.Subscriber(
            'computer_vision/braitenberg',
            Point,
            queue_size=1,
            callback=self.vision_values_received
        )

        self.publisher = rospy.Publisher(
            'pid/references',
            Twist,
            queue_size=1
        )

        self.sensor_l = 0
        self.sensor_r = 0

        self.steering = 0
        self.throttle = 0
        self.twist = Twist()
    
    def vision_values_received(self, data):
        
        pass


if __name__ == '__main__':
    rospy.init_node('navigation')

    navigation = Navigation()

    rospy.spin()
