execute_process(COMMAND "C:/Users/aheto/Documents/research/catkin_ws/catkin_ws_remote/build/tada-ros/catkin_generated/python_distutils_install.bat" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(C:/Users/aheto/Documents/research/catkin_ws/catkin_ws_remote/build/tada-ros/catkin_generated/python_distutils_install.bat) returned error code ")
endif()
