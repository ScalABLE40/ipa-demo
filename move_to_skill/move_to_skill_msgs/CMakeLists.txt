cmake_minimum_required(VERSION 2.8.3)
project(move_to_skill_msgs)

find_package(catkin REQUIRED COMPONENTS
  actionlib_msgs
  message_generation
  std_msgs
  geometry_msgs 
)

add_action_files(
  FILES
  MoveToSkill.action
)

generate_messages(
  DEPENDENCIES
  actionlib_msgs std_msgs geometry_msgs 
)

catkin_package(
 CATKIN_DEPENDS actionlib_msgs std_msgs geometry_msgs 
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)
