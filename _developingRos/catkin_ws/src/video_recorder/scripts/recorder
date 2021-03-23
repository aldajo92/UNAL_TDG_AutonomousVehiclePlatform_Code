#!/usr/bin/python

import rospy
import cv2

from sensor_msgs.msg import Joy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

from datetime import datetime

class VideoRecorderController(object):
    def __init__(self):
        self.buttonCapture = 0
        self.bridge = CvBridge()
        self.BGR = None
        self.shape = None

        self.videoWriter = None
        self.recording = True

        self.joySubscriber = rospy.Subscriber("joy", Joy, self.joyCallback)
        self.imgSubscriber = rospy.Subscriber(
            'camera_processing/camera/image_color/BGR/raw',
            Image,
            queue_size=1,
            callback=self.imageCallback)
    
    def joyCallback(self, data):
        buttonValue = data.buttons[1]
        self.buttonCapture = buttonValue

        if self.buttonCapture == 1:
            if self.videoWriter == None:
                frame_height = self.shape[0]
                frame_width = self.shape[1]
                filename = '/catkin_ws/'+ self._generateVideoFileName()
                rospy.loginfo(filename)
                self.videoWriter = cv2.VideoWriter(
                    filename,
                    cv2.VideoWriter_fourcc('M','J','P','G'), 
                    18,
                    (frame_width,frame_height))
                rospy.loginfo("capturing")
        else:
            if self.videoWriter != None:
                self.videoWriter.release()
                self.videoWriter = None
                rospy.loginfo("releasing")
    
    def imageCallback(self, msg):
        img = self.bridge.imgmsg_to_cv2(msg)
        self.BGR = img

        if self.shape == None:
            self.shape = img.shape
            rospy.loginfo(img.shape)
            rospy.loginfo(img.shape[0])
            rospy.loginfo(img.shape[1])
        
        if self.videoWriter != None:
            self.videoWriter.write(self.BGR)
    
    def _generateVideoFileName(self):
        now = datetime.now()
        dt_string = now.strftime("%d%m%Y_%H%M%S.avi")
        return dt_string


def main():
    rospy.init_node("recorder")
    obj = VideoRecorderController()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")

if __name__ == "__main__":
    main()