import rclpy

from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from geometry_msgs.msg import Twist

class DrawCircleNode(Node):
    def __init__(self):
        super().__init__('draw_circle')
        self.cmd_vel_publisher_ = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.get_logger().info('Draw circle node started')
        self.create_timer(0.5, self.send_velocity_command)

    def send_velocity_command(self):
        msg = Twist()
        msg.linear.x = 2.0 #sped
        msg.angular.z = 1.0
        self.cmd_vel_publisher_.publish(msg)
    

def main(args=None):
    try:
        with rclpy.init(args=args):
            node = DrawCircleNode()
            rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass

if __name__ == '__main__':
    main()
