@echo off

if DEFINED DESTDIR (
  echo "Destdir.............%DESTDIR%"
  set DESTDIR_ARG="--root=%DESTDIR%"
)

cd "C:/Users/the1k/source/repos/PythonApplication1/catkin_ws_remote/src/tada-ros"

if NOT EXIST "C:\Users\the1k\source\repos\PythonApplication1\catkin_ws_remote\install\lib/site-packages\" (
  mkdir "C:\Users\the1k\source\repos\PythonApplication1\catkin_ws_remote\install\lib/site-packages"
)

set "PYTHONPATH=C:\Users\the1k\source\repos\PythonApplication1\catkin_ws_remote\install\lib/site-packages;C:/Users/the1k/source/repos/PythonApplication1/catkin_ws_remote/build\lib/site-packages"
set "CATKIN_BINARY_DIR=C:/Users/the1k/source/repos/PythonApplication1/catkin_ws_remote/build"
for /f "usebackq tokens=*" %%a in ('C:\Users\the1k\source\repos\PythonApplication1\catkin_ws_remote\install') do (
  set _SETUPTOOLS_INSTALL_PATH=%%~pna
  set _SETUPTOOLS_INSTALL_ROOT=%%~da
)

"C:/opt/ros/noetic/x64/python.exe" ^
    "C:/Users/the1k/source/repos/PythonApplication1/catkin_ws_remote/src/tada-ros\setup.py" ^
    build --build-base "C:/Users/the1k/source/repos/PythonApplication1/catkin_ws_remote/build/tada-ros" ^
    install %DESTDIR_ARG%  ^
    --prefix="%_SETUPTOOLS_INSTALL_PATH%" ^
    --install-scripts="%_SETUPTOOLS_INSTALL_PATH%\bin" ^
    --root=%_SETUPTOOLS_INSTALL_ROOT%\
