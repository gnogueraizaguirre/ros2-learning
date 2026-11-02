cmake_minimum_required(VERSION 3.20)
project(cpp_pubsub)

# Default to C++20
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 20)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

#Add Exec
add_executable(talker src/publisher_lambda_function.cpp)
target_link_libraries(talker PUBLIC rclcpp::rclcpp std_msgs::std_msgs)

add_executable(listener src/subscriber_lambda_function.cpp)
target_link_libraries(listener PUBLIC rclcpp::rclcpp std_msgs::std_msgs)

install(TARGETS
  talker
  listener
  DESTINATION lib/${PROJECT_NAME})
  
ament_package()
