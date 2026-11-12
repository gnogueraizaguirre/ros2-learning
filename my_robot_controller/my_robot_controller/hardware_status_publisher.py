#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from my_robot_interfaces.msg import HardwareStatus
 
 
class HardwareStatusPublisherNode(Node):
    def __init__(self):
        super().__init__("hardware_status_publisher")
        self.hardware_status_pub_ = self.create_publisher(HardwareStatus,"hardware_status",10)
        self.timer_ = self.create_timer(1.0, self.publish_status)
        self.get_logger().info("Publisher has been started")

    def publish_status(self):
        msg = HardwareStatus()
        msg.temperature = 30.5
        msg.motors_ready = True
        msg.debug_message = "nothing to report"
        self.hardware_status_pub_.publish(msg)

 
 
def main(args=None):
    rclpy.init(args=args)
    node = HardwareStatusPublisherNode()
    rclpy.spin(node)
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()