#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
 
 
class PublisherNode(Node): 
    def __init__(self):
        super().__init__("Numbers_Node") 
        self.number_publisher = self.create_publisher(Int32,"numbers",10)
        self.get_logger().info("Publisher Started")
        self.number_timer = self.create_timer(1.0,  self.timer_callback)
        self.get_logger().info("Timer Started")
        self.counter = 0

    def timer_callback(self):
        self.counter += 1
        msg = Int32()
        msg.data = self.counter
        self.number_publisher.publish(msg)
 
 
def main(args=None):
    rclpy.init(args=args)
    node = PublisherNode() 
    rclpy.spin(node)
    rclpy.shutdown()
 
 
if __name__ == "_main_":
    main()