# Install script for directory: C:/Users/the1k/source/repos/PythonApplication1/catkin_ws/src/xsens_mti_driver

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "C:/Users/the1k/source/repos/PythonApplication1/catkin_ws/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "RelWithDebInfo")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "C:/Users/the1k/source/repos/PythonApplication1/catkin_ws/build/xsens_mti_driver/catkin_generated/installspace/xsens_mti_driver.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/xsens_mti_driver/cmake" TYPE FILE FILES
    "C:/Users/the1k/source/repos/PythonApplication1/catkin_ws/build/xsens_mti_driver/catkin_generated/installspace/xsens_mti_driverConfig.cmake"
    "C:/Users/the1k/source/repos/PythonApplication1/catkin_ws/build/xsens_mti_driver/catkin_generated/installspace/xsens_mti_driverConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/xsens_mti_driver" TYPE FILE FILES "C:/Users/the1k/source/repos/PythonApplication1/catkin_ws/src/xsens_mti_driver/package.xml")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/xsens_mti_driver" TYPE EXECUTABLE FILES "C:/Users/the1k/source/repos/PythonApplication1/catkin_ws/devel/lib/xsens_mti_driver/xsens_mti_node.exe")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/xsens_mti_driver" TYPE EXECUTABLE FILES "C:/Users/the1k/source/repos/PythonApplication1/catkin_ws/devel/lib/xsens_mti_driver/configure_outputs.exe")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/xsens_mti_driver" TYPE DIRECTORY FILES
    "C:/Users/the1k/source/repos/PythonApplication1/catkin_ws/src/xsens_mti_driver/launch"
    "C:/Users/the1k/source/repos/PythonApplication1/catkin_ws/src/xsens_mti_driver/param"
    )
endif()

