#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
import random
 
 #ros2 run Activity02_Publisher_py number_publisher  --ros-args -p timer_length:=2.0 ... -p idkman:=idk
class PublisherNode(Node): 
    def __init__(self):
        super().__init__("Numbers_Node") 

        # Parameters
        self.declare_parameter("timer_length",1.0)
        self.declare_parameter("number_min", 1)
        self.declare_parameter("number_max", 100)

        # Variables
        self.timer_length_ = self.get_parameter("timer_length").value
        self.number_min_ = self.get_parameter("number_min").value
        self.number_max_ = self.get_parameter("number_max").value

        self.number_publisher = self.create_publisher(Int32,"numbers",10)
        self.get_logger().info("Publisher Started")
        self.number_timer = self.create_timer(self.timer_length_,  self.timer_callback)
        self.get_logger().info("Timer Started")

    def timer_callback(self):
        number = random.randint(self.number_min_, self.number_max_)
        msg = Int32()
        msg.data = number
        self.number_publisher.publish(msg)
 
 
def main(args=None):
    rclpy.init(args=args)
    node = PublisherNode() 
    rclpy.spin(node)
    rclpy.shutdown()
 
 
if __name__ == "_main_":
    main()