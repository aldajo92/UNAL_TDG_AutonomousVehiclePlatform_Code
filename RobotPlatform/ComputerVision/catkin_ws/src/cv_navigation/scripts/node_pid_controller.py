#!/usr/bin/env python3

import rospy

from geometry_msgs.msg import Point
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32
from sensor_msgs.msg import MagneticField

'''
PIDController for throttle
kp:
ki:
kd:
'''
class PIDController:

    def __init__(self, kp, ki, kd, max_u):
        self.reference = 0.0
        self.measure = 0.0

        self.kp = kp
        self.ki = ki
        self.kd = kd

        self.error = 0          # Proportional
        self.int_error = 0      # Integral
        self.prev_error = 0     # Derivative
        self.diff_error = 0      # Derivative

        self.max_control_action = max_u
        self.min_control_action = 0

    
    def calculate_pid_control_signal(self):
        self.prev_error = self.error

        self.error = self.reference - self.measure
        if abs(self.error) < (self.reference*0.05):
            self.error = 0

        self.int_error += self.error
        self.diff_error = self.error - self.prev_error

        u_p = self.kp * self.error
        u_i = self.ki * self.int_error
        u_d = self.kd * self.diff_error

        u_signal = 0.5 + u_p + u_i + u_d

        rospy.loginfo("error: {}".format(self.error))

        # apply boundaries
        if u_signal > self.max_control_action:
            u_signal = self.max_control_action

        if self.reference == 0.0:
            u_signal = 0
        
        if u_signal < 0:
            u_signal = 0

        return u_signal

class PIDNode:

    def __init__(self):
        self._rate = rospy.Rate(2)
        self.pid_throttle = PIDController(0.5, 0.1, 0.001, 0.8)

        self.motor_publishser = rospy.Publisher(
            "motors/motor_twist",
            Twist,
            queue_size=1
        )
        self.pid_subscriber = rospy.Subscriber(
            "pid/references",
            Twist,
            queue_size=1,
            callback=self.references_values_received
        )

        self.enconder_subscriber = rospy.Subscriber(
            "magnet_encoder/value",
            Float32,
            queue_size=1,
            callback=self.encoder_value_received
        )

        self.start_filter = False
        self.last_measure = 0

        # self.imu_subscriber = rospy.Subscriber(
        #     "imu/mag",
        #     MagneticField,
        #     queue_size=1,
        #     callback=self.magnet_sensor_received
        # )

        self.twist_motor = Twist()
    
    def references_values_received(self, twist_ref):
        self.pid_throttle.reference = twist_ref.linear.x
        self.twist_motor.angular.z = twist_ref.angular.z
        rospy.loginfo("ref: {}".format(self.pid_throttle.reference))
    
    def encoder_value_received(self, float32):
        current_measure = float32.data
        if self.start_filter:
            self.pid_throttle.measure = (current_measure + self.last_measure)/2
        else:
            self.pid_throttle.measure = current_measure
            self.start_filter = True
        self.last_measure = current_measure
    
    def run_pid_loop(self):
        while not rospy.is_shutdown():
            u_throttle = self.pid_throttle.calculate_pid_control_signal()
            self.twist_motor.linear.x = u_throttle

            if self.pid_throttle.reference != 0:
                self.motor_publishser.publish(self.twist_motor)
            self._rate.sleep()

if __name__ == '__main__':
    rospy.init_node('pid_controller') # No finished yet
    pidNode = PIDNode()
    pidNode.run_pid_loop()
    rospy.spin()
