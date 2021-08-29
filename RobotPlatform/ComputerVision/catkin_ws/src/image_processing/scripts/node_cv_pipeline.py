#!/usr/bin/env python3

import rospy

from sensor_msgs.msg import Image
from geometry_msgs.msg import Point
from cv_bridge import CvBridge
import cv2
import numpy as np

import library_braitenberg as br
# import library_lane_detection as ld

class CVProcessingNode(object):

    def __init__(self):
        self.imgSubscriber = rospy.Subscriber(
            'camera/BGR/raw',
            Image,
            queue_size=1,
            callback=self.onImageReceived
        )

        self.imgBinaryPublisher = rospy.Publisher(
            'computer_vision/braitenberg',
            Image,
            queue_size=1
        )

        self.navPublisher = rospy.Publisher(
            'braitenberg/values',
            Point,
            queue_size=1
        )

        self.bridge = CvBridge()
        corners_region_l, corners_region_r = br.getLeftRightCorners(240, 320)

        self.braitenberg = br.Braitenberg(corners_region_l, corners_region_r, 80)
        self.braitenbergValues = Point()
        self.braitenbergValues.z = 0
        
        # self.corners = ld.getCorners(240, 320)
        # self.lane_processing = ld.LaneDetection(self.corners)

        # input image
        self.BGR = np.zeros(shape=(0,0))
    
    def onImageReceived(self, msg):
        self.BGR = self.bridge.imgmsg_to_cv2(msg)
    
    def processImage(self, image):
        # BGR = cv2.resize(BGR, (320, 240))

        # result = self.lane_processing.process_image(image)
        img_regions, activation_l, activation_r = self.braitenberg.process_image(image)
        self.braitenbergValues.x = activation_l
        self.braitenbergValues.y = activation_r

        self.imgBinaryPublisher.publish(
            self.bridge.cv2_to_imgmsg(img_regions, 'bgr8'))

        # mono8
        # mono8, bgr8
        # self.imgBinaryPublisher.publish(
        #     self.bridge.cv2_to_imgmsg(result, 'bgr8'))
    
    def cv_loop(self):
        rate = rospy.Rate(2)
        while not rospy.is_shutdown():
            if self.BGR.shape != (0,0):
                self.processImage(self.BGR)
                self.navPublisher.publish(self.braitenbergValues)
            rate.sleep()

if __name__ == '__main__':
    rospy.init_node('camera_processing_python3')

    cv_node = CVProcessingNode()
    cv_node.cv_loop()

    rospy.spin()
