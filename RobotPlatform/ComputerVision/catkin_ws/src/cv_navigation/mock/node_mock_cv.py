#!/usr/bin/env python3

import rospy

from sensor_msgs.msg import Image
from geometry_msgs.msg import Point
import cv2

class CVProcessingNode:

    def __init__(self):
        self._rate = rospy.Rate(1)

        self._navPublisher = rospy.Publisher(
            'braitenberg/values',
            Point,
            queue_size=1
        )

        self._mock_data = [(100,100), (100,0), (0,100), (0,0)]
        self._mock_index = 0
        self.b_point = Point()
    
    def cv_loop(self):
        while not rospy.is_shutdown():
            index = self._mock_index
            self.b_point.x = self._mock_data[index][0]
            self.b_point.y = self._mock_data[index][1]
            self.b_point.z = 0

            self._navPublisher.publish(self.b_point)
            self._mock_index = (self._mock_index + 1) % 4
            self._rate.sleep()

if __name__ == '__main__':
    rospy.init_node('moc_braitenberg')

    cv_node = CVProcessingNode()
    cv_node.cv_loop()

    rospy.spin()
