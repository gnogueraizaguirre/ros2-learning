#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from my_robot_interfaces.msg import Turtles
from my_robot_interfaces.msg import Turtle
from turtlesim_msgs.srv import Spawn
from turtlesim_msgs.srv import Kill
import random

from functools import partial # Without this i cant pass the request to the future callback
 
class TurtleSpawnerNode(Node):
    def __init__(self):
        super().__init__("turtle_spawner")
        # Parametres
        self.declare_parameter("timer",1.0)

        # Variables
        self.spawner_timer_ = self.create_timer(self.get_parameter("timer").value ,self.spawn_turtle) #
        self.get_logger().info("Timer started with period of " + str(self.get_parameter("timer").value))
        self.turtle_list_ = Turtles()

        # Pubsub
        self.turtle_publisher_ = self.create_publisher(Turtles,"turtle_positions",10)


        
        #self.kill_client_ = self.create_client(Kill, "/kill")

    def spawn_turtle(self):
        self.client_ = self.create_client(Spawn, "/spawn") # Im not sure if it makes more sense to create this in the init or here
        while not self.client_.wait_for_service(1.):
            self.get_logger().warning("Waiting for service")

        if len(self.turtle_list_._turtles) < 5:

            turtle_ = Turtle() # I shoulve made this a Spawn Request message
            request = Spawn.Request()
            turtle_.x = request.x = random.uniform(1,11)
            turtle_.y = request.y =random.uniform(1,11)
            turtle_.theta = request.theta = random.uniform(1,11)
            turtle_.name = request.name = "turtle" + str(len(self.turtle_list_.turtles))

            future = self.client_.call_async(request)
            future.add_done_callback(partial(self.spawn_turtle_callback, turtle = turtle_))
    
    def spawn_turtle_callback(self, future, turtle):
        result = future.result()
        self.get_logger().info(str(result))
        self.turtle_list_.turtles.append(turtle)
        self.get_logger().info("Turtle List :\n" + str(self.turtle_list_.turtles))
        
        
 
def main(args=None):
    rclpy.init(args=args)
    node = TurtleSpawnerNode()
    rclpy.spin(node)
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()