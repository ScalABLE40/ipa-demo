cmake_minimum_required(VERSION 2.8.3)
project(locate_object_skill_server)

find_package(catkin REQUIRED COMPONENTS
  actionlib
  rospy
  roscpp
  locate_object_skill_msgs
)

catkin_python_setup()

catkin_package(
 CATKIN_DEPENDS rospy actionlib locate_object_skill_msgs
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)
