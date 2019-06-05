# Minimum CMake required
cmake_minimum_required(VERSION 3.10)

find_package(PythonInterp 3.5 REQUIRED)
find_package(PythonLibs 3.5 REQUIRED)

set(PROGRESSIVE_SRCS
	src/progressive.c	
)

add_library(progressive SHARED ${PROGRESSIVE_SRCS})
target_link_libraries(progressive ${PYTHON_LIBRARY} libfreerdp)
target_include_directories(progressive PRIVATE ${PYTHON_INCLUDE_DIR})

set_target_properties(progressive PROPERTIES
	PREFIX ""
	OUTPUT_NAME "progressive"
)
