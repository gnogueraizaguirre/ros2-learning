cmake_minimum_required(VERSION 3.20)
project(add_two_ints_cpp)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(example_interfaces REQUIRED)

add_executable(addTwoInts_service src/addTwoInts_service.cpp)
target_include_directories(addTwoInts_service PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include/${PROJECT_NAME}>)
target_compile_features(addTwoInts_service PUBLIC c_std_17 cxx_std_20)  # Require C17 and C++20
target_link_libraries(
  addTwoInts_service
  ${rclcpp_TARGETS}
  ${example_interfaces_TARGETS}
)

add_executable(addTwoInts_client src/addTwoInts_client.cpp)
target_link_libraries(
  addTwoInts_client
  ${rclcpp_TARGETS}
  ${example_interfaces_TARGETS}
)

install(TARGETS 
  addTwoInts_service
  addTwoInts_client
  DESTINATION lib/${PROJECT_NAME})

ament_package()
