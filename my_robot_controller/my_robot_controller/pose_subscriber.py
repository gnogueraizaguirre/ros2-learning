import rclpy

from rclpy.node import Node
from turtlesim_msgs.msg import Pose


class PoseSubscriberNode(Node):
	"""docstring for PoseSubscriberNode"""
	def __init__(self):
		super().__init__("pose_subscriber")
		self.pose_subscriber_ = self.create_subscription(Pose,"/turtle1/pose", self.pose_callback,10)

	def pose_callback(self,msg):
		self.get_logger().info("(x: {}, y: {}, theta: {})".format(msg.x,msg.y,msg.theta))


def main(args=None):
	try:
		with rclpy.init(args=args):
			node = PoseSubscriberNode()
			rclpy.spin(node)
	except KeyboardInterrupt:
		pass


