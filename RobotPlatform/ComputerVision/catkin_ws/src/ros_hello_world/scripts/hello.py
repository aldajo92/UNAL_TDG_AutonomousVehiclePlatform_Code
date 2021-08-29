#!/usr/bin/env python3

import rospy

from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

def talker():
    pub = rospy.Publisher('hello', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        hello_str = "hello world %s" % rospy.get_time()
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
        rate.sleep()

class CameraProcessing(object):

    def __init__(self):
        self.imgSubscriber = rospy.Subscriber(
            'camera_processing/camera/image_color/BGR/raw',
            Image,
            queue_size=1,
            callback=self.onImageReceived
        )

        self.imgBinaryPublisher = rospy.Publisher(
            'camera_processing/camera/image_result/raw',
            Image,
            queue_size=1
        )

        self.bridge = CvBridge()

        # input image
        self.BGR = None
    
    def onImageReceived(self, msg):
        self.BGR = self.bridge.imgmsg_to_cv2(msg)
        self.processImage(self.BGR)
    
    def processImage(self, BGR):
        # reduce the resolution of the image to half to allow for
        # faster processing
        BGR = cv2.resize(BGR, (320, 240))

        # convert image to HSV
        HSV = cv2.cvtColor(BGR, cv2.COLOR_BGR2HSV)

        self.imgBinaryPublisher.publish(
            self.bridge.cv2_to_imgmsg(HSV, 'bgr8'))

if __name__ == '__main__':
    rospy.init_node('camera_processing_python3')

    processor = CameraProcessing()

    rospy.spin()
