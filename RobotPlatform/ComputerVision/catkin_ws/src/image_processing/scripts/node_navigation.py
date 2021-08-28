#!/usr/bin/env python3

import rospy

from geometry_msgs.msg import Point
from geometry_msgs.msg import Twist

class Navigation:

    def __init__(self, threshold):

        self.subscriber = rospy.Subscriber(
            'braitenberg/values',
            Point,
            queue_size=1,
            callback=self.values_received
        )

        self.threshold = threshold

        self.publisher = rospy.Publisher(
            'pid/references',
            Twist,
            queue_size=1
        )

        self.steering_max = 0.5
        self.throttle_ref = 0.5
        self.twist = Twist()
    
    def values_received(self, point):
        value_l = point.x
        value_r = point.y
        if value_l > threshold and value_r > self.threshold:
            self.twist.linear.x = 0
            self.twist.angular.z = 0
        elif value_l > threshold and value_r <= self.threshold:
            self.twist.linear.x = self.throttle_ref
            self.twist.angular.z = 0.5
        elif if value_l <= threshold and value_r > self.threshold:
            self.twist.linear.x = self.throttle_ref
            self.twist.angular.z = -0.5
        else:
            self.twist.linear.x = self.throttle_ref
            self.twist.angular.z = 0

        self.publisher.publish(self.twist)
        # TODO: Remove log line if its not longer used
        # rospy.loginfo("x = {}, y = {}".format(point.x, point.y))
    

if __name__ == '__main__':
    rospy.init_node('navigation')

    navigation = Navigation(80)

    rospy.spin()
