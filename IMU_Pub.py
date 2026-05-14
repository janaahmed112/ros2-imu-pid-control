import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu


class PublishPosition(Node):
    def __init__(self):
       super().__init__("Publish_Acc")

       self.declare_parameter("acc_x",0.0)
       self.acc_pub = self.create_publisher(Imu,'imu_topic',10)
       self.timer =self.create_timer(0.5,self.publish_position)
       self.get_logger().info("Publish Acceleration node has been started")

    def publish_position(self):
        msg = Imu()

        acc_x=self.get_parameter("acc_x").value
        msg.linear_acceleration.x=float(acc_x)
        msg.linear_acceleration.y=0.0
        msg.linear_acceleration.z=9.81

        self.acc_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = PublishPosition()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()    





