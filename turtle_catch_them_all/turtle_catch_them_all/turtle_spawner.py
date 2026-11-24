#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from my_robot_interfaces.msg import Turtles
from my_robot_interfaces.msg import Turtle
from turtlesim_msgs.srv import Spawn
from turtlesim_msgs.srv import Kill
from turtlesim_msgs.msg import Pose
import random
import math

from functools import partial # Without this i cant pass the request to the future callback
 
class TurtleSpawnerNode(Node):
    def __init__(self):
        super().__init__("turtle_spawner")
        # Parametres
        self.declare_parameter("timer",0.5)
        self.declare_parameter("turtles", 5)

        # Variables
        self.turtle_list_ = Turtles()
        self.my_turtle_pose = Pose()

        # Pubsub
        self.turtle_publisher_ = self.create_publisher(Turtles,"turtle_positions",10)
        self.my_turtle_subscriber_ = self.create_subscription(Pose, "my_turtle/pose", self.update_my_turtle_pose,10)

        # Clients
        self.kill_client_ = self.create_client(Kill, "/kill")
        self.spawn_client_ = self.create_client(Spawn, "/spawn")
        
        # Startup: It waits until the /kill service is up to clear turtlesim and start my own spawner process
        self.startup_timer_ = self.create_timer(0.1, self.clear_turtlesim)


    def status_update_(self): 
        # Variables
        self.turtles_vector_ = [(turtle.x, turtle.y, turtle.name) for turtle in self.turtle_list_.turtles] # Vector containing the data i need for collision detection. Angle is ignored
        min_distance = 0.75  # min distance for /kill

        # Do i need to spawn more turtles?
        if len(self.turtle_list_.turtles) < self.get_parameter("turtles").value:  #How many?
            self.spawn_turtle()

        # Obtain the movement target
        for turtle in self.turtles_vector_:
            distance = math.sqrt((turtle[0] - self.my_turtle_pose.x)**2 + (turtle[1] - self.my_turtle_pose.y)**2) ## Pythagoras to calc distance. The controller doesn't care about the turtle name, even though the info is there
            if distance < min_distance:
                request = Kill.Request()
                request.name = turtle[2]
                future = self.kill_client_.call_async(request)
                #self.get_logger().warning(f"Turtle Killed: {turtle[2]}")
                future.add_done_callback(partial(self.kill_turtle_callback, request = request))

    def kill_turtle_callback(self,future, request):
        try:
            future.result()
            self.turtle_list_.turtles = [
                turtle for turtle in self.turtle_list_.turtles
                if turtle.name != request.name
            ]
            self.get_logger().warning(f"Turtle killed: {request.name}")
            self.turtle_publisher_.publish(self.turtle_list_)

        except Exception as e:
            self.get_logger().error(f"Failed to kill {request.name}: {e}")


 
    def update_my_turtle_pose(self, pose : Pose):
        self.my_turtle_pose.x = pose.x
        self.my_turtle_pose.y = pose.y
        self.my_turtle_pose.theta = pose.theta

    def spawn_turtle(self, x = None, y = None, theta = None, name = None, initial = False):

        # Random values unless specified
        x = x if x is not None else random.uniform(1, 11)
        y = y if y is not None else random.uniform(1, 11)
        theta = theta if theta is not None else random.uniform(0, 2 * math.pi)
        name = name if name is not None else ("")

        if not self.spawn_client_.service_is_ready():
            self.get_logger().warning("Spawn service not available")
            return

        turtle_ = Turtle() # I shoulve made this a Spawn Request message
        request = Spawn.Request()
        turtle_.x = request.x = x
        turtle_.y = request.y = y
        turtle_.theta = request.theta = theta
        turtle_.name = request.name = name
        future = self.spawn_client_.call_async(request)
        future.add_done_callback(partial(self.spawn_turtle_callback, turtle = turtle_, initial = initial))

    
    def spawn_turtle_callback(self, future, turtle, initial):
        result = future.result()
        if initial:
            self.status_update_timer_ = self.create_timer(1.0, self.status_update_)
        else:
            turtle.name = result.name
            self.turtle_list_.turtles.append(turtle)

            if len(self.turtle_list_.turtles) >= self.get_parameter("turtles").value:
                self.turtle_publisher_.publish(self.turtle_list_)

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

        self.spawn_turtle(5.544445,5.544445,0.0, "my_turtle", True)

        
 
def main(args=None):
    rclpy.init(args=args)
    node = TurtleSpawnerNode()
    rclpy.spin(node)
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()