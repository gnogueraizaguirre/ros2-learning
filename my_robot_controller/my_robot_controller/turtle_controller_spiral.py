# This was supposed to be a simple pubsub controller but i thought about making a spiral
import rclpy

from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim_msgs.msg import Pose 
from turtlesim_msgs.srv import SetPen
from functools import partial


import math # omg math hii


# Actually a golden spiral. It'll be constant angular velocity and growing linear
# so radial velocity = a*e^(b*theta)
phi = (1 + math.sqrt(5)) / 2
pi = math.pi # approx 3
b = 1 * math.log(phi) / pi #it should be 2x but i want more spins per turtle
a = 0.25


class TurtleControllerNode(Node):
    def __init__(self):
        # Setup
        super().__init__("turtle_controller")
        self.get_logger().info("Turtle Controller Node started")

        # PubSub Stuff
        self.pose_subscriber_ = self.create_subscription(Pose, "/turtle1/pose", self.pose_callback, 10)
        self.pose_publisher_ = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)

        # Variable for tracking the total angular movement
        self.previous_theta_ = None
        self.total_angle_ = 0.0
        self.right_= False

    def pose_callback(self, pos : Pose):
        # Logging fluff
        #self.get_logger().info(f"Pose: x={pos.x}, y={pos.y}, theta={pos.theta}")

        # Command the movement of turtle boy
        # Accumulated angular displacement? sounds mathy enough 
        if self.previous_theta_ is not None:
            delta = (pos.theta - self.previous_theta_ + math.pi) % (2 * math.pi) - math.pi
            self.total_angle_ += delta

        self.previous_theta_ = pos.theta

        # Calculate velocity
        cmd_vel = Twist()

        cmd_vel.linear.x = a * math.exp(b * self.total_angle_) * math.sqrt(1 + b**2)
        cmd_vel.angular.z = 1.0

        # It was kinda sad watching turtle boy hit the screen. This stops it
        if pos.x <= 0.5 or pos.x >= 10.5 or pos.y <= 0.5 or pos.y >= 10.5:
            self.get_logger().info("Boundaries.")

            cmd_vel.linear.x = 0.0
            cmd_vel.angular.z = 0.0

            self.pose_publisher_.publish(cmd_vel)
            rclpy.shutdown() # Goodnight sweet prince
            return
        self.pose_publisher_.publish(cmd_vel)

        #Changes the colour depending on hemisphere
        if pos.x > 5.5 and self.right_ == False:
            self.get_logger().info("Switching to red")
            self.call_set_pen_service(255,0,0,3,0)
            self.right_ = True

        elif pos.x <= 5.5 and self.right_ == True:
            self.get_logger().info("Switching to Blue")
            self.call_set_pen_service(0,0,255,3,0)
            self.right_ = False

    def call_set_pen_service(self, r,g,b,width,off):
        client = self.create_client(SetPen,"/turtle1/set_pen")

        # Wait for service
        while not client.wait_for_service(1.0):
            self.get_logger.warn("Waiting for service")


        # Request data
        request = SetPen.Request()
        request.r = r
        request.g = g
        request.b = b
        request.width = width
        request.off = off

        future = client.call_async(request)
        future.add_done_callback(partial(self.callback_set_pen))

    def callback_set_pen(self, future):
        try:
            response = future.result()

        except Exception as e:
            self.get_logger().error("Service call failed %r" % (e,))


def main(args=None):
    try:
        with rclpy.init(args=args):
            node = TurtleControllerNode()
            rclpy.spin(node) # why did they even named this spin
    except KeyboardInterrupt:
        pass


