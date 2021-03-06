# /****************************************************************************
#  *   Copyright (c) 2017 Michael Shomin. All rights reserved.
#  *
#  * Redistribution and use in source and binary forms, with or without
#  * modification, are permitted provided that the following conditions
#  * are met:
#  *
#  * 1. Redistributions of source code must retain the above copyright
#  *    notice, this list of conditions and the following disclaimer.
#  * 2. Redistributions in binary form must reproduce the above copyright
#  *    notice, this list of conditions and the following disclaimer in
#  *    the documentation and/or other materials provided with the
#  *    distribution.
#  * 3. Neither the name ATLFlight nor the names of its contributors may be
#  *    used to endorse or promote products derived from this software
#  *    without specific prior written permission.
#  *
#  * NO EXPRESS OR IMPLIED LICENSES TO ANY PARTY'S PATENT RIGHTS ARE GRANTED BY THIS LICENSE.
#  * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
#  * FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
#  * COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
#  * INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
#  * BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
#  * OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
#  * AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
#  * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
#  * ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#  * POSSIBILITY OF SUCH DAMAGE.
#  *
#  * In addition Supplemental Terms apply.  See the SUPPLEMENTAL file.
#  ****************************************************************************/

cmake_minimum_required(VERSION 2.8.3)
project(snav_ros)

find_package(catkin REQUIRED COMPONENTS
  cmake_modules
  geometry_msgs
  std_msgs
  rosgraph_msgs
  roscpp
  tf2
  tf2_ros
  tf2_geometry_msgs
  snav_msgs
  dynamic_reconfigure
)

if ("${QC_SOC_TARGET}" STREQUAL "APQ8096")
  add_definitions( -DQC_SOC_TARGET_APQ8096 )
  message("Building for APQ8096")
else()
  add_definitions( -DQC_SOC_TARGET_APQ8074 )
  message("Building for APQ8074")
endif()


## System dependencies are found with CMake's conventions
find_package(Boost REQUIRED COMPONENTS system)

generate_dynamic_reconfigure_options(cfg/SnavRos.cfg)

catkin_package(
  INCLUDE_DIRS include
  CATKIN_DEPENDS geometry_msgs rosgraph_msgs roscpp tf2 tf2_ros tf2_geometry_msgs snav_msgs
  DEPENDS system_lib
)

###########
## Build ##
###########

## Specify additional locations of header files
## Your package locations should be listed before other locations
include_directories(
  include
  ${catkin_INCLUDE_DIRS}
  snav
  snav_fci
  /usr/include/eigen3
)

set(CMAKE_CXX_FLAGS "-std=c++11 ${CMAKE_CXX_FLAGS}")

add_library(snav_fci SHARED snav_fci/imp/src/flight_control_interface.cpp
  snav_fci/imp/src/planner.cpp
  snav_fci/imp/src/waypoint.cpp
)

target_link_libraries(snav_fci snav_arm snav_traj_gen)

add_library(snav_interface
  src/snav_interface.cpp)
add_dependencies(snav_interface
  ${catkin_EXPORTED_TARGETS})
add_dependencies(snav_interface
  ${PROJECT_NAME}_gencfg)

## Declare a C++ executable
add_executable(snav_interface_node
  src/snav_interface_node.cpp)
add_dependencies(snav_interface_node
  ${PROJECT_NAME}_gencfg)

## Specify libraries to link a library or executable target against
target_link_libraries(snav_interface
   ${catkin_LIBRARIES}
   snav_arm
   snav_fci
)

target_link_libraries(snav_interface_node
   ${catkin_LIBRARIES}
   snav_interface
)

add_custom_command(
TARGET snav_interface_node
COMMAND echo "Setting the UID bit for the node to run with root privileges"
COMMAND sudo chown root ${CATKIN_DEVEL_PREFIX}/lib/snav_ros/snav_interface_node
COMMAND sudo chmod +s ${CATKIN_DEVEL_PREFIX}/lib/snav_ros/snav_interface_node
)

install(TARGETS snav_interface_node snav_interface
  ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

## Mark other files for installation (e.g. launch and bag files, etc.)
install(FILES
  DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
)
