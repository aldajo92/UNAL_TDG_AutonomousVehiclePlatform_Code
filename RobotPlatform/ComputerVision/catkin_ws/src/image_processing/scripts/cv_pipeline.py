#!/usr/bin/env python3

import rospy

from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

import lane_detection_pipeline as pipeline

def talker():
    pub = rospy.Publisher('hello', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        hello_str = "hello world %s" % rospy.get_time()
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
        rate.sleep()

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

class CameraProcessing(object):

    def __init__(self):
        self.imgSubscriber = rospy.Subscriber(
            'camera/BGR/raw',
            Image,
            queue_size=1,
            callback=self.onImageReceived
        )

        self.imgBinaryPublisher = rospy.Publisher(
            'computer_vision/line_processing',
            Image,
            queue_size=1
        )

        self.bridge = CvBridge()
        self.corners = getCorners(240, 320)
        self.lane_processing = pipeline.LaneDetection(self.corners)

        # input image
        self.BGR = None
    
    def onImageReceived(self, msg):
        self.BGR = self.bridge.imgmsg_to_cv2(msg)
        self.processImage(self.BGR)
    
    def processImage(self, image):
        # reduce the resolution of the image to half to allow for
        # faster processing
        # BGR = cv2.resize(BGR, (320, 240))

        # process images
        result = self.lane_processing.process_image(image)

        # HSV = cv2.cvtColor(BGR, cv2.COLOR_BGR2HSV)

        self.imgBinaryPublisher.publish(
            self.bridge.cv2_to_imgmsg(result, 'bgr8'))

        # mono8
        # bgr8
        # self.imgBinaryPublisher.publish(
        #     self.bridge.cv2_to_imgmsg(result, 'bgr8'))

if __name__ == '__main__':
    rospy.init_node('camera_processing_python3')

    processor = CameraProcessing()

    rospy.spin()
