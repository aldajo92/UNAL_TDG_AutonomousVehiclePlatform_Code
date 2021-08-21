#define _USE_MATH_DEFINES
#define N_MAGNETS 16
#define SAMPLE_TIME 200     // ms
#define DIAMETER 120        // mm

#include <ros/ros.h>
#include <cstdlib>
#include <cerrno>
#include <cstring>
#include <sys/ioctl.h>

#include <unistd.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <linux/i2c-dev.h>
#include <std_msgs/Float32.h>
#include <cmath>

class I2CReadWrite
{
public:
    int i2cPort;
    unsigned char buffer[2];

    void setup(char *id, int addr)
    {
        char *i2cPortName = id;
        if ((i2cPort = open(i2cPortName, O_RDWR)) < 0)
        {
            ROS_FATAL("Failed to open the i2c bus");
        }

        if (ioctl(i2cPort, I2C_SLAVE, addr) < 0)
        {
            ROS_FATAL("Failed to acquire bus access and/or talk to slave.\n");
        }
        return;
    }

    unsigned char *readi2cData(int length)
    {
        // string res;
        if (read(i2cPort, buffer, length) != length)
        {
            ROS_FATAL("Failed to read from the i2c bus.\n");
            return NULL;
        }
        // int measure = (int) buffer[0];
        // printf("Data read: %d\n", measure);
        return buffer;
    }
    
    void writeBytes(unsigned char* dataRequest, int length)
    {
        if (write(i2cPort, dataRequest, length) != length)
        {
            printf("Failed to write to the i2c bus.\n");
        }
    }
};

int main(int argc, char **argv)
{
    ros::NodeHandle *nh = NULL;
    ros::NodeHandle *nh_priv = NULL;

    I2CReadWrite *i2c = new I2CReadWrite();

    ros::init(argc, argv, "magnet_encoder_node");

    nh = new ros::NodeHandle();
    if (!nh)
    {
        ROS_FATAL("Failed to initialize NodeHandle");
        ros::shutdown();
        return -1;
    }

    nh_priv = new ros::NodeHandle("~");
    if (!nh_priv)
    {
        ROS_FATAL("Failed to initialize private NodeHandle");
        delete nh;
        ros::shutdown();
        return -2;
    }

    // taken from https://github.com/ros-industrial/cros/blob/master/resources/cros_testbed/src/std_msgs_talker.cpp
    ros::Publisher measure_publisher_value = nh->advertise<std_msgs::Float32>("magnet_encoder/value", 1000);

    char i2cPathName[] = "/dev/i2c-1";
    int i2cAddress = 0x04;

    i2c->setup(i2cPathName, i2cAddress);

    // activity = new imu_bno055::BNO055I2CActivity(*nh, *nh_priv);
    // watchdog = new watchdog::Watchdog();

    // if(!activity) {
    //     ROS_FATAL("Failed to initialize driver");
    //     delete nh_priv;
    //     delete nh;
    //     ros::shutdown();
    //     return -3;
    // }

    // if(!activity->start()) {
    //     ROS_ERROR("Failed to start activity");
    //     delete nh_priv;
    //     delete nh;
    //     ros::shutdown();
    //     return -4;
    // }

    int param_freq;
    nh_priv->param("freq", param_freq, (int)5);
    // ROS_INFO("freq = %d", freq);

    ros::Rate rate(param_freq);
    unsigned char cmd[] = {0x01};
    std_msgs::Float32 velocity_value;

    while (ros::ok())
    {
        i2c->writeBytes(cmd, 1);
        usleep(200);
        
        int measure = (int) (i2c->readi2cData(1)[0]);
        
        velocity_value.data = (measure*M_PI*DIAMETER)/(N_MAGNETS*SAMPLE_TIME);
        measure_publisher_value.publish(velocity_value);

        // ROS_INFO("Data read: %.3f\n", velocity_value.data);

        rate.sleep();
    }

    // activity->stop();

    // delete watchdog;
    delete i2c;
    delete nh_priv;
    delete nh;

    return 0;
}
