import rclpy

from rclpy.node import Node
from rclpy.executors import ExternalShutdownException


class MyNode(Node):
    def __init__(self):
        super().__init__('first_node')
        self.get_logger().info('Ros2 node initialized')
        self.counter_ = 0
        self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        self.get_logger().info('hi ' + str(self.counter_))
        self.counter_ += 1


def main(args=None):
    try:
        with rclpy.init(args=args):
            node = MyNode()
            rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass

if __name__ == '__main__':
    main()