project(Home_work_2_Chernovol)

cmake_minimum_required(VERSION 3.0)
set(CMAKE_VERBOSE_MAKEFILE on)

find_package(PythonLibs 3.2 REQUIRED)


include_directories(${PYTHON_INCLUDE_DIRS})

python_add_module(my_module main.cpp)
target_link_libraries(my_module ${PYTHON_LIBRARIES})
