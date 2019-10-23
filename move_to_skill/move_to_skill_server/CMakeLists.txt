cmake_minimum_required(VERSION 2.8.3)
project(move_to_skill_server)

find_package(catkin REQUIRED COMPONENTS
  actionlib
  rospy
  roscpp
  move_to_skill_msgs
)

catkin_python_setup()

catkin_package(
 CATKIN_DEPENDS rospy actionlib move_to_skill_msgs
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)
