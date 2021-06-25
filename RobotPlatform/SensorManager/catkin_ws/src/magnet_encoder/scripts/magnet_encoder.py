#!/usr/bin/python

import mardan_msgs.srv as msrv
import rospy
import smbus


# global variables
i2cBus = None


# def i2cServiceCallback(request):
#     global i2cBus
    
#     if len(request.dataIn) > 0:
        
#         data = [ord(c) for c in request.dataIn]
#         i2cBus.write_i2c_block_data(request.slaveAddress, 0, data)
    
    
#     if request.bytesToRead > 0:
        
#         response = msrv.i2cResponse()
#         response.dataOut = i2cBus.read_i2c_block_data(request.slaveAddress, 0, request.bytesToRead)
#         return response
    
#     return msrv.i2cResponse()
    

if __name__ == '__main__':
    
    rospy.init_node('i2c_master')
    rospy.loginfo('i2c_master start')
    
    i2cBus = smbus.SMBus(1)
    
    rospy.Service('magnet_encoder/raw', msrv.i2c, i2cServiceCallback)
    
    rospy.spin()