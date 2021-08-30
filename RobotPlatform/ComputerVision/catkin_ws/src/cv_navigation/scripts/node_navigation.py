#!/usr/bin/env python3

import rospy

from geometry_msgs.msg import Point
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy

class Navigation:

    def __init__(self, threshold):

        self.subscriber = rospy.Subscriber(
            'braitenberg/values',
            Point,
            queue_size=1,
            callback=self.values_received
        )

        # TODO: Change joy by other topic
        self.subscriber = rospy.Subscriber(
            'joy',
            Joy,
            queue_size=1,
            callback=self.joy_received
        )

        self.threshold = threshold

        self.publisher = rospy.Publisher(
            'pid/references',
            Twist,
            queue_size=1
        )

        self.steering_ref = 0.5
        self.throttle_ref = 0.3
        self.twist = Twist()
        self._stop_point = Point(100,100,0)
        self.activate_navigation = False
    
    def joy_received(self, joy_data):
        button_x = joy_data.buttons[7]
        button_y = joy_data.buttons[6]
        
        if button_x == 1:
            self.activate_navigation = True
        else:
            self.activate_navigation = False

        if button_y == 1:
            self.activate_navigation = False
            self._stop_reference()
        
        rospy.loginfo("x = {}".format(button_x))

    def values_received(self, b_point):
        if self.activate_navigation :
            self._navigation_movement(b_point)
    
    def _navigation_movement(self, point):
        value_l = point.x
        value_r = point.y
        if value_l > self.threshold and value_r > self.threshold:
            self.twist.linear.x = 0
            self.twist.angular.z = 0
        elif value_l > self.threshold and value_r <= self.threshold:
            self.twist.linear.x = self.throttle_ref
            self.twist.angular.z = -self.steering_ref
        elif value_l <= self.threshold and value_r > self.threshold:
            self.twist.linear.x = self.throttle_ref
            self.twist.angular.z = self.steering_ref
        else:
            self.twist.linear.x = self.throttle_ref
            self.twist.angular.z = 0

        self.publisher.publish(self.twist)
    
    def _stop_reference(self):
        self.twist.linear.x = 0
        self.twist.angular.z = 0
        self.publisher.publish(self.twist)


if __name__ == '__main__':
    rospy.init_node('navigation')

    navigation = Navigation(80)

    rospy.spin()
