#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from my_robot_interfaces.srv import Switch
 
 
class BatteryNode(Node):
    def __init__(self):
        super().__init__("battery_node")
        self.battery_timer_ = self.create_timer(1, self.battery_update_callback)
        self.update_timer_ = self.create_timer(1, self.update_led_timer_callback) # This causes repeated messages
        self.charge_ = 100
        self.charging_ = False ## So i can tell if it should be charging or discharging
        self.ledClient_ = self.create_client(Switch, "switch_led_panel")

    def battery_update_callback(self):
        self.get_logger().info(f"Battery level: {self.charge_}%")
        # Charge/Discharge cycle
        if self.charging_ == False:
            self.charge_ -= 20
            if self.charge_ == 0:
                self.charging_ = True
        else:
            self.charge_ += 10
            if self.charge_ == 100:
                self.charging_ = False

    def update_led_timer_callback(self):
        if not self.ledClient_.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn("LED service not available, waiting again...")
            return
        request = Switch.Request()
        if self.charge_  == 0:
            request.led_number = 2
            request.status = True
            future = self.ledClient_.call_async(request)
            future.add_done_callback(self.led_response_callback)
        elif self.charge_ == 100:
            request.led_number = 2
            request.status = False
            future = self.ledClient_.call_async(request)
            future.add_done_callback(self.led_response_callback)

    def led_response_callback(self, future):
        try:
            response = future.result()
            self.get_logger().info(f"LED service response: {response}")
        except Exception as e:
            self.get_logger().error(f"Service call failed: {e}")
        

def main(args=None):
    rclpy.init(args=args)
    node = BatteryNode()
    rclpy.spin(node)
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()