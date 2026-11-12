#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from my_robot_interfaces.srv import Cubicate
 
 
class CubeVolumeNode(Node):
    def __init__(self):
        super().__init__("Cubicator")
        self.server_ = self.create_service(Cubicate, "Cubicate", self.cubicatorCallback)
        self.get_logger().info("node started")

    def cubicatorCallback(self, request : Cubicate.Request, response : Cubicate.Response):
        response.area = request.length * request.width
        response.volume = response.area * request.height
        self.get_logger().info(f"Area {request.length} x {request.width} = {response.area}m²")
        self.get_logger().info(f"Volume {request.length} x {request.width} x {request.height}= {response.volume}m³")
        return response
 
def main(args=None):
    rclpy.init(args=args)
    node = CubeVolumeNode()
    rclpy.spin(node)
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()