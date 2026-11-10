cmake_minimum_required(VERSION 3.20)
project(Activity02_counter_cpp)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(example_interfaces REQUIRED)

# Executables
add_executable(counter src/counter.cpp)
target_link_libraries(counter PUBLIC
rclcpp::rclcpp
std_msgs::std_msgs
example_interfaces::example_interfaces
)

install(TARGETS
  counter
  DESTINATION lib/${PROJECT_NAME}
)
ament_package()
