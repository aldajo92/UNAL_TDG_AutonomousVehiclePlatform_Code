#!/usr/bin/env python3

import rospy

from geometry_msgs.msg import Point

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

    
    def apply_control_signal(self, reference, sensor_value):
        self.error = reference - sensor_value
        self.int_error += self.int_error + self.error
        self.der_error = self.error - self.prev_error

        # apply boundaries


if __name__ == '__main__':
    rospy.init_node('pid_controller') # No finished yet

    pid = PIDController(1,1,1)

    rospy.spin()
