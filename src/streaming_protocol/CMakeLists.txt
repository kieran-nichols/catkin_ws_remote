cmake_minimum_required(VERSION 2.8.3)
project(streaming_protocol)

# for similar compile https://github.com/ros/ros_comm/blob/noetic-devel/clients/roscpp/CMakeLists.txt

## Compile as C++11, supported in ROS Kinetic and newer
#set(CMAKE_CXX_STANDARD 11)
#add_compile_options(-std=c++11)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
  roscpp
  cpp_common
  roscpp_serialization 
  std_msgs
)

## System dependencies are found with CMake's conventions
# find_package(Boost REQUIRED COMPONENTS system)


## Uncomment this if the package has a setup.py. This macro ensures
## modules and global scripts declared therein get installed
## See http://ros.org/doc/api/catkin/html/user_guide/setup_dot_py.html
# catkin_python_setup()

################################################
## Declare ROS messages, services and actions ##
################################################

## To declare and build messages, services or actions from within this
## package, follow these steps:
## * Let MSG_DEP_SET be the set of packages whose message types you use in
##   your messages/services/actions (e.g. std_msgs, actionlib_msgs, ...).
## * In the file package.xml:
##   * add a build_depend tag for "message_generation"
##   * add a build_depend and a exec_depend tag for each package in MSG_DEP_SET
##   * If MSG_DEP_SET isn't empty the following dependency has been pulled in
##     but can be declared for certainty nonetheless:
##     * add a exec_depend tag for "message_runtime"
## * In this file (CMakeLists.txt):
##   * add "message_generation" and every package in MSG_DEP_SET to
##     find_package(catkin REQUIRED COMPONENTS ...)
##   * add "message_runtime" and every package in MSG_DEP_SET to
##     catkin_package(CATKIN_DEPENDS ...)
##   * uncomment the add_*_files sections below as needed
##     and list every .msg/.srv/.action file to be processed
##   * uncomment the generate_messages entry below
##   * add every package in MSG_DEP_SET to generate_messages(DEPENDENCIES ...)

## Generate messages in the 'msg' folder
# add_message_files(
#   FILES
#   Message1.msg
#   Message2.msg
# )

## Generate added messages and services with any dependencies listed here
# generate_messages(
#   DEPENDENCIES
#   std_msgs
# )

###################################
## catkin specific configuration ##
###################################
## The catkin_package macro generates cmake config files for your package
## Declare things to be passed to dependent projects
## INCLUDE_DIRS: uncomment this if your package contains header files
## LIBRARIES: libraries you create in this project that dependent projects also need
## CATKIN_DEPENDS: catkin_packages dependent projects also need
## DEPENDS: system dependencies of this project that dependent projects also need

catkin_package(CATKIN_DEPENDS roscpp std_msgs)

###########
## Build ##
###########

#link_directories(lib/xspublic/xscontroller lib/xspublic/xscommon lib/xspublic/xstypes)
link_directories(lib)

## Specify additional locations of header files
## Your package locations should be listed before other locations
include_directories(
  include
  #lib/xspublic
  lib
  ${catkin_INCLUDE_DIRS}
)

set (SOURCES 
			centerofmassdatagram.cpp
			parsermanager.cpp
			jointanglesdatagram.cpp
			angularsegmentkinematicsdatagram.cpp
			centerofmassdatagram.cpp
			datagram.cpp
			eulerdatagram.cpp
			linearsegmentkinematicsdatagram.cpp
			main.cpp
			metadatagram.cpp
			positiondatagram.cpp
			quaterniondatagram.cpp
			scaledatagram.cpp
			streamer.cpp
			timecodedatagram.cpp
			trackerkinematicsdatagram.cpp
			udpserver.cpp
)

set(HEADERS 
			centerofmassdatagram.h
			parsermanager.h
			jointanglesdatagram.h
			angularsegmentkinematicsdatagram.h
			centerofmassdatagram.h
			datagram.h
			eulerdatagram.h
			linearsegmentkinematicsdatagram.h
			metadatagram.h
			positiondatagram.h
			quaterniondatagram.h
			scaledatagram.h
			streamer.h
			timecodedatagram.h
			trackerkinematicsdatagram.h
			udpserver.h
)

#add_custom_target(xspublic
#  COMMAND +make -C ${CMAKE_CURRENT_SOURCE_DIR}/lib/xspublic
#)

## Declare a C++ executable
## With catkin_make all packages are built within a single CMake context
## The recommended prefix ensures that target names across packages don't collide
add_executable(${PROJECT_NAME}_node ${SOURCES} ${HEADERS})



## Specify libraries to link a library or executable target against
#target_link_libraries(
#	${PROJECT_NAME}_node
#	PUBLIC 
#	xscontroller
#	xscommon
#	xstypes
#	pthread
#	dl
#	${catkin_LIBRARIES}
#)

#add_dependencies(roscpp ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})

target_link_libraries(
	${PROJECT_NAME}_node
	PUBLIC 
	xstypes64
#	xstypes64.dll
	${catkin_LIBRARIES}
	${CMAKE_DL_LIBS}
	#${CATKIN_GLOBAL_BIN_DESTINATION}
	#roscpp 
)

install(TARGETS ${PROJECT_NAME}_node
   ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
   LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
   RUNTIME DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
)

install(TARGETS ${PROJECT_NAME}_node
   RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

#file(COPY lib/xstypes64.dll DESTINATION devel/lib/streaming_protocol/)
#copy dll file from source to devel folder; couldn't successfully copy the file into the devel/lib folder
# you can get file from Xsens\Xsens MVN Developer Toolkit 1.2.0\Examples\prebuilt\x64
#add_custom_command(
#	TARGET ${PROJECT_NAME} POST_BUILD
#	COMMAND ${CMAKE_COMMAND} -E copy 
#		"{CMAKE_CURRENT_SOURCE_DIR}/bin/xstypes64.dll" 
#	 	"devel/lib/streaming_protocol/xstypes64.dll" ) #$<TARGET_FILE_DIR:${PROJECT_NAME}>)



