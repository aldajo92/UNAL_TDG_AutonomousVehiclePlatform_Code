#!/usr/bin/env python3

import rospy

from geometry_msgs.msg import Point
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32
from sensor_msgs.msg import MagneticField

class PIDController:

    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd

        self.current_value = 0
        self.error = 0
        self.prev_error = 0
        self.int_error = 0
        self.der_error = 0

        self.max_control_action = 0
        self.min_control_action = 0

    
    def apply_pid_control_signal(self, reference, sensor_value):
        pass
        # self.error = reference - sensor_value
        # self.int_error += self.int_error + self.error
        # self.der_error = self.error - self.prev_error
        # apply boundaries

class PIDNode:

    def __init__(self):
        self.pid = PIDController(1,1,1)

        self.publishser = rospy.Publisher(
            "motors/motor_twist",
            Twist,
            queue_size=1
        )
        self.subscriber = rospy.Subscriber(
            "pid/references",
            Twist,
            queue_size=1,
            callback=self.references_values_received
        )

        self.subscriber = rospy.Subscriber(
            "magnet_encoder/value",
            Float32,
            queue_size=1,
            callback=self.encoder_value_received
        )

        self.subscriber = rospy.Subscriber(
            "imu/mag",
            MagneticField,
            queue_size=1,
            callback=self.magnet_sensor_received
        )
    
    def references_values_received(self, twist):
        # TODO: add implementation for reference values received
        pass
    
    def encoder_value_received(self, float32):
        # TODO: add implementation for encoder values received
        pass
    
    def magnet_sensor_received(self, magnet):
        # TODO: add implementation for magnet values received
        pass
    
    def run_pid_loop(self):
        rate = rospy.Rate(10) # 10hz
        while not rospy.is_shutdown():
            # hello_str = "hello world %s" % rospy.get_time()
            # rospy.loginfo(hello_str)
            pid.apply_pid_control_signal()
            rate.sleep()

if __name__ == '__main__':
    rospy.init_node('pid_controller') # No finished yet
    pid = PIDNode()
    pid.run_pid_loop()
    rospy.spin()
