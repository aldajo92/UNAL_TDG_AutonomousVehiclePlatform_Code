#!/usr/bin/env python3

import rospy

from sensor_msgs.msg import Image
from geometry_msgs.msg import Point
from cv_bridge import CvBridge
import cv2
import numpy as np

import library_lane_detection as pipeline
import library_braitenberg as br


def getCorners(height, width):
    mid_offset = 20
    bottom_offset = 0
    x_offset = 0
    y_bottom_offset = 130
    y_top_offset = 65

    mid_y = height // 2
    mid_width = width // 2

    left_bottom = (0 + bottom_offset + x_offset, height - y_bottom_offset)
    right_bottom = (width - bottom_offset + x_offset, height - y_bottom_offset)
    apex1 = ( mid_width - mid_offset + x_offset, mid_y - y_top_offset)
    apex2 = ( mid_width + mid_offset + x_offset, mid_y - y_top_offset)
    corners = [left_bottom, right_bottom, apex2, apex1]

    return corners

def getLeftRightCorners(height, width):
    rectange_w = 10
    rectange_h = 40

    margin_horizontal = 100
    margin_top = 70

    corners_region_l = [
        (margin_horizontal, margin_top),
        (margin_horizontal, rectange_h+margin_top),
        (margin_horizontal+rectange_w, rectange_h+margin_top),
        (margin_horizontal+rectange_w, margin_top)
    ]
    corners_region_r = [
        (width-margin_horizontal-rectange_w, margin_top), 
        (width-margin_horizontal-rectange_w, rectange_h+margin_top),
        (width-margin_horizontal, rectange_h+margin_top),
        (width-margin_horizontal, margin_top)
    ]
    return corners_region_l, corners_region_r

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
        self.corners = getCorners(240, 320)

        corners_region_l, corners_region_r = getLeftRightCorners(240, 320)
        self.braitenberg = br.Braitenberg(corners_region_l, corners_region_r, 80)
        self.braitenbergValues = Point()
        
        # self.lane_processing = pipeline.LaneDetection(self.corners)

        # input image
        self.BGR = np.zeros(shape=(0,0))
    
    def onImageReceived(self, msg):
        self.BGR = self.bridge.imgmsg_to_cv2(msg)
    
    def processImage(self, image):
        # BGR = cv2.resize(BGR, (320, 240))

        # result = self.lane_processing.process_image(image)
        activation_l, activation_r = self.braitenberg.process_image(image)
        self.braitenbergValues.x = activation_l
        self.braitenbergValues.y = activation_r
        self.braitenbergValues.z = 0

        self.imgBinaryPublisher.publish(
            self.bridge.cv2_to_imgmsg(image, 'bgr8'))

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
