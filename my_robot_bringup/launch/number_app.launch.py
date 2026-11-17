from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld= LaunchDescription()

    number_publisher = Node(
        package="Activity02_Publisher_py"
        executable="number_publisher"
    )
    number_counter = Node(
        package="Activity02_counter_cpp"
        executable="counter"
    )
    ld.add_action(number_publisher)
    ld.add_action(number_counter)
    return ld