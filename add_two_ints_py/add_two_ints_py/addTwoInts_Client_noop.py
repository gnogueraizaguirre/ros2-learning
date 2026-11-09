#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts
 
def main(args=None):
    rclpy.init(args=args)
    node = Node("numbers_client_noop_py")
    client = node.create_client(AddTwoInts, "AddTwoInts_py")

    while not client.wait_for_service(1.):
        node.get_logger().warn("Waiting for service")
    node.get_logger().info("Service found")
    request = AddTwoInts.Request()
    request.a = 40
    request.b = 2

    future = client.call_async(request)
    rclpy.spin_until_future_complete(node, future)

    response = future.result()
    node.get_logger().info(str(request.a) + " + " + str(request.b) + " = " + str(response.sum))
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()