# Install script for directory: C:/Users/the1k/source/repos/PythonApplication1/catkin_ws/src/soem/SOEM

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
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY FILES "C:/Users/the1k/source/repos/PythonApplication1/catkin_ws/devel/lib/soem.lib")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/soem" TYPE FILE FILES
    "C:/Users/the1k/source/repos/PythonApplication1/catkin_ws/src/soem/SOEM/soem/ethercat.h"
    "C:/Users/the1k/source/repos/PythonApplication1/catkin_ws/src/soem/SOEM/soem/ethercatbase.h"
    "C:/Users/the1k/source/repos/PythonApplication1/catkin_ws/src/soem/SOEM/soem/ethercatcoe.h"
    "C:/Users/the1k/source/repos/PythonApplication1/catkin_ws/src/soem/SOEM/soem/ethercatconfig.h"
    "C:/Users/the1k/source/repos/PythonApplication1/catkin_ws/src/soem/SOEM/soem/ethercatconfiglist.h"
    "C:/Users/the1k/source/repos/PythonApplication1/catkin_ws/src/soem/SOEM/soem/ethercatdc.h"
    "C:/Users/the1k/source/repos/PythonApplication1/catkin_ws/src/soem/SOEM/soem/ethercateoe.h"
    "C:/Users/the1k/source/repos/PythonApplication1/catkin_ws/src/soem/SOEM/soem/ethercatfoe.h"
    "C:/Users/the1k/source/repos/PythonApplication1/catkin_ws/src/soem/SOEM/soem/ethercatmain.h"
    "C:/Users/the1k/source/repos/PythonApplication1/catkin_ws/src/soem/SOEM/soem/ethercatprint.h"
    "C:/Users/the1k/source/repos/PythonApplication1/catkin_ws/src/soem/SOEM/soem/ethercatsoe.h"
    "C:/Users/the1k/source/repos/PythonApplication1/catkin_ws/src/soem/SOEM/soem/ethercattype.h"
    "C:/Users/the1k/source/repos/PythonApplication1/catkin_ws/src/soem/SOEM/osal/osal.h"
    "C:/Users/the1k/source/repos/PythonApplication1/catkin_ws/src/soem/SOEM/osal/win32/inttypes.h"
    "C:/Users/the1k/source/repos/PythonApplication1/catkin_ws/src/soem/SOEM/osal/win32/osal_defs.h"
    "C:/Users/the1k/source/repos/PythonApplication1/catkin_ws/src/soem/SOEM/osal/win32/osal_win32.h"
    "C:/Users/the1k/source/repos/PythonApplication1/catkin_ws/src/soem/SOEM/osal/win32/stdint.h"
    "C:/Users/the1k/source/repos/PythonApplication1/catkin_ws/src/soem/SOEM/oshw/win32/nicdrv.h"
    "C:/Users/the1k/source/repos/PythonApplication1/catkin_ws/src/soem/SOEM/oshw/win32/oshw.h"
    )
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("C:/Users/the1k/source/repos/PythonApplication1/catkin_ws/build/soem/SOEM/test/linux/slaveinfo/cmake_install.cmake")
  include("C:/Users/the1k/source/repos/PythonApplication1/catkin_ws/build/soem/SOEM/test/linux/eepromtool/cmake_install.cmake")
  include("C:/Users/the1k/source/repos/PythonApplication1/catkin_ws/build/soem/SOEM/test/linux/simple_test/cmake_install.cmake")

endif()

