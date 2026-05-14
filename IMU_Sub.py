import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu


class ImuSub(Node):
    def __init__(self):
        super().__init__("IMU_SUB")
        self.lasttime = self.get_clock().now()
        self.setpoint_x=0.0
        self.last_error=0
        self.integral=0
        self.kp=2
        self.ki=0.5
        self.kd=0.1
        self.imu_sub=self.create_subscription(Imu,'imu_topic',self.imuacc,10)

    def imuacc(self,msg:Imu):
        
        
        currenttime= self.get_clock().now()
        dt_n = (currenttime - self.lasttime) 
        dt = dt_n.nanoseconds / 1e9

        acc_x= msg.linear_acceleration.x
        accx = (acc_x/16384.0)*9.81
        read_value = accx
        error = self.setpoint_x - read_value
        propotional = error
        self.integral +=error*dt
        if dt == 0 : return 
        derivative = (error - self.last_error)/dt
        
        read = (self.kp * error ) + (self.ki * self.integral) + (self.kd * derivative)
        self.get_logger().info(f"The PID value : {read}")

        self.last_error = error
        self.lasttime = currenttime


def main(args=None):
    rclpy.init(args=args)
    node = ImuSub()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()


