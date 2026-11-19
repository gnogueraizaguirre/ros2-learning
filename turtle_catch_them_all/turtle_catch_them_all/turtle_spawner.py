#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from my_robot_interfaces.msg import Turtles
from my_robot_interfaces.msg import Turtle
from turtlesim_msgs.srv import Spawn
from turtlesim_msgs.srv import Kill
import random
import math

from functools import partial # Without this i cant pass the request to the future callback
 
class TurtleSpawnerNode(Node):
    def __init__(self):
        super().__init__("turtle_spawner")
        # Parametres
        self.declare_parameter("timer",1.0)

        # Variables
        self.turtle_list_ = Turtles()

        # Pubsub
        self.turtle_publisher_ = self.create_publisher(Turtles,"turtle_positions",10)

        # Clients
        self.kill_client_ = self.create_client(Kill, "/kill")
        self.spawn_client_ = self.create_client(Spawn, "/spawn")
        
        # Startup: It waits until the /kill service is up to clear turtlesim and start my own spawner process
        self.startup_timer_ = self.create_timer(0.1, self.clear_turtlesim)
    def status_update_(self): #
        pass

    def spawn_turtle(self, x = None, y = None, theta = None, name = None):

        # Random values unless specified
        x = x if x is not None else random.uniform(1, 11)
        y = y if y is not None else random.uniform(1, 11)
        theta = theta if theta is not None else random.uniform(0, 2 * math.pi)
        name = name if name is not None else "turtle" + str(len(self.turtle_list_.turtles))

        # Wait for the /spawn service
        while not self.spawn_client_.wait_for_service(1.):
            self.get_logger().warning("Waiting for service")


        if len(self.turtle_list_._turtles) < 6:

            turtle_ = Turtle() # I shoulve made this a Spawn Request message
            request = Spawn.Request()
            turtle_.x = request.x = x
            turtle_.y = request.y = y
            turtle_.theta = request.theta = theta
            turtle_.name = request.name = "turtle" + str(len(self.turtle_list_.turtles))

            future = self.spawn_client_.call_async(request)
            future.add_done_callback(partial(self.spawn_turtle_callback, turtle = turtle_))
    
    def spawn_turtle_callback(self, future, turtle):
        result = future.result()
        self.get_logger().info(str(result))
        self.turtle_list_.turtles.append(turtle)
        self.get_logger().info("Turtle List :\n" + str(self.turtle_list_.turtles))

    def clear_turtlesim(self):
        if not self.kill_client_.service_is_ready():
            self.get_logger().info("Waiting for kill service...")
            return

        self.startup_timer_.cancel()
        request = Kill.Request()
        request.name = "turtle1"

        future = self.kill_client_.call_async(request)
        future.add_done_callback(self.clear_turtlesim_callback)

    def clear_turtlesim_callback(self, future):
        try:
            future.result()
            self.get_logger().info("Turtlesim cleared!")

        except Exception as e:
            self.get_logger().error(f"Failed to clear turtlesim: {e}")
            return

        self.spawn_turtle(5.544445,5.544445,0.0, "my_turtle")
        self.status_update_timer_ = self.create_timer(1,self.status_update_) # Main looping function

        
 
def main(args=None):
    rclpy.init(args=args)
    node = TurtleSpawnerNode()
    rclpy.spin(node)
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()