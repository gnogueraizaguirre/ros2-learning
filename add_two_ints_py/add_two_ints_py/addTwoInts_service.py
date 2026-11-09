#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts
 
 
class AddTwoIntsServerNode(Node): 
    def __init__(self):
        super().__init__("Add_Two_Ints_Python_Server")
        self.server_ = self.create_service(AddTwoInts,"AddTwoInts_py",self.serviceCallback)
        self.get_logger().info("Add two ints server has started")

    def serviceCallback(self, request : AddTwoInts.Request, response : AddTwoInts.Response):
        response.sum = request.a + request.b #Declaring the sum
        self.get_logger().info(str(request.a) + " + " + str(request.b) + " = " + str(response.sum))
        return response
 
 
def main(args=None):
    rclpy.init(args=args)
    node = AddTwoIntsServerNode() 
    rclpy.spin(node)
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()