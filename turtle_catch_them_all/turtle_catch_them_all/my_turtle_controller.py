#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from my_robot_interfaces.msg import Turtles
from my_robot_interfaces.msg import Turtle
from geometry_msgs.msg import Twist
from turtlesim_msgs.msg import Pose 
import math
 
class MyTurtleController(Node):
    def __init__(self):
        super().__init__("my_turtle_controller")

        # Parametres

        # Variables
        self.turtles_msg_= Turtles()
        self.turtles_vector_= []

        # Pubsub
        self.turtles_subscriber_ = self.create_subscription(Turtles,"turtle_positions", self.new_turtle_callback, 10)
        self.my_turtle_pose_subscriber_ = self.create_subscription(Pose, "my_turtle/pose", self.my_turtle_pose_callback, 10)
        self.my_turtle_vel_publisher_ = self.create_publisher(Twist,"my_turtle/cmd_vel",10)
        

    def my_turtle_pose_callback(self, pose : Pose):
        if not self.turtles_vector_: # Don't bother until this vector is populated
            return
        
        # Variables
        min_distance = float('inf')
        distance = float()
        target_pos_x = 5.544445
        target_pos_y = 5.544445
        Kp_linear_ = 1.0 # Proportional constant
        Kp_angular_ = 5.0
        
        # Obtain the movement target
        for turtle in self.turtles_vector_:
            distance = math.sqrt((turtle[0] - pose.x)**2 + (turtle[1] - pose.y)**2) ## Pythagoras to calc distance. The controller doesn't care about the turtle name, even though the info is there
            if distance < min_distance:
                min_distance = distance
                target_pos_x = turtle[0]
                target_pos_y = turtle[1]
        #self.get_logger().info(f"Min distance: {min_distance}") #Logging

        # Movement Vector. This is a target, not the ideal or the real
        delta_x = target_pos_x - pose.x
        delta_y = target_pos_y - pose.y
        target_angle = math.atan2(delta_y, delta_x)

        angle_error = math.atan2(math.sin(target_angle - pose.theta),math.cos(target_angle - pose.theta)) # Diff between current angle and target, normalized.
                                 
        # My Turtle Vector
        my_turtle_vel = Twist()
        my_turtle_vel.linear.x = Kp_linear_ * min_distance
        my_turtle_vel.angular.z = Kp_angular_ * angle_error
        self.my_turtle_vel_publisher_.publish(my_turtle_vel)

    def new_turtle_callback(self, turtle_list : Turtles):
        self.turtles_vector_ = [(turtle.x, turtle.y, turtle.name) for turtle in turtle_list.turtles] # Vector containing the data i need for collision detection. Angle is ignored
        self.get_logger().warning("New turtles:")
        self.get_logger().info(str(self.turtles_vector_))
            

 
 
def main(args=None):
    rclpy.init(args=args)
    node = MyTurtleController()
    rclpy.spin(node)
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()