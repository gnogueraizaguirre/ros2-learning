cmake_minimum_required(VERSION 3.20)
project(my_cpp_robot_controller)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

# Executables
add_executable(my_first_cpp_node src/my_first_node.cpp)
target_link_libraries(my_first_cpp_node PUBLIC
rclcpp::rclcpp 
std_msgs::std_msgs)

install(TARGETS
  my_first_cpp_node
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
