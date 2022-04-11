cmake_minimum_required(VERSION 3.0.2)
project(uwb)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  message_generation
)

## Generate messages in the 'msg' folder
add_message_files(
  FILES
  tag_distance.msg
  uwb_Position.msg
)
## Generate added messages and services with any dependencies listed here
generate_messages(
  DEPENDENCIES
  std_msgs
)

catkin_package(
 CATKIN_DEPENDS 
 roscpp 
 rospy 
 std_msgs 
 message_runtime
)

###########
## Build ##
###########
include_directories(
  include
  ${catkin_INCLUDE_DIRS}
)


add_executable(uwb_positioning src/Position.cpp src/uwb_positioning.cpp)

add_executable(eigen_test src/eigen_test.cpp)

target_link_libraries(uwb_positioning
  ${catkin_LIBRARIES}
)
add_dependencies(uwb_positioning
  ${catkin_EXPORTED_TARGETS}
)

#############
## Install ##
#############

install(PROGRAMS
  scripts/uwb_start.py
  scripts/cal_std_mean.py
  scripts/preprocess.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(TARGETS
  uwb_positioning
  ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
  )

# install(DIRECTORY include/${PROJECT_NAME}/
#   DESTINATION ${CATKIN_PACKAGE_INCLUDE_DESTINATION}
# )

