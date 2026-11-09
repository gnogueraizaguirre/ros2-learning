#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts
from functools import partial # Without this i cant pass the request to the future callback
 
class addTwoIntsClientNode(Node):
    def __init__(self):
        super().__init__("addTwoInts_client_node")
        self.client_ = self.create_client(AddTwoInts, "AddTwoInts_py")
        #self.timer_ = self.create_timer(1.0,self.timerCallback)
        self.get_logger().info("Client Started")

    def callAddTwoInts(self, a , b):
        while not self.client_.wait_for_service(1.):
            self.get_logger().warn("Waiting for service")
        request = AddTwoInts.Request()
        request.a = a
        request.b = b

        future = self.client_.call_async(request)
        future.add_done_callback(partial(self.callback_addTwoInts, request = request))

    def callback_addTwoInts(self, future, request):
        result = future.result()
        self.get_logger().info(str(request.a) + " + " + str(request.b) + " = " + str(result.sum))

 
def main(args=None):
    rclpy.init(args=args)
    node = addTwoIntsClientNode()
    node.callAddTwoInts(60, 7)
    node.callAddTwoInts(60, 9)
    node.callAddTwoInts(601234523, 91234)
    rclpy.spin(node)
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()