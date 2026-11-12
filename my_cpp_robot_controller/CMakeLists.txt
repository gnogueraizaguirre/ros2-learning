cmake_minimum_required(VERSION 3.20)
project(my_cpp_robot_controller)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(my_robot_interfaces REQUIRED)

# Executables
add_executable(my_first_cpp_node src/my_first_node.cpp)
target_link_libraries(my_first_cpp_node PUBLIC
rclcpp::rclcpp)

add_executable(my_cpp_publisher src/my_cpp_publisher.cpp)
target_link_libraries(my_cpp_publisher PUBLIC
rclcpp::rclcpp 
std_msgs::std_msgs)

add_executable(subscriber src/my_cpp_subscriber.cpp)
target_link_libraries(subscriber PUBLIC
rclcpp::rclcpp 
std_msgs::std_msgs)

add_executable(clock src/clock.cpp)
target_link_libraries(clock PUBLIC
rclcpp::rclcpp 
std_msgs::std_msgs)

add_executable(hw_status_publisher src/hardware_status_publisher.cpp)
target_link_libraries(hw_status_publisher PUBLIC
rclcpp::rclcpp 
my_robot_interfaces::my_robot_interfaces)

install(TARGETS
  my_first_cpp_node
  my_cpp_publisher
  subscriber
  clock
  hw_status_publisher
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
