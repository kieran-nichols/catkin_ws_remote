execute_process(COMMAND "C:/Users/the1k/source/repos/PythonApplication1/catkin_ws/build/tada-ros/catkin_generated/python_distutils_install.bat" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(C:/Users/the1k/source/repos/PythonApplication1/catkin_ws/build/tada-ros/catkin_generated/python_distutils_install.bat) returned error code ")
endif()