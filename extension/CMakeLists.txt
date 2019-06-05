# Minimum CMake required
cmake_minimum_required(VERSION 3.10)

# Project
project(python-freerdp LANGUAGES C VERSION 1.0.0)

# Config
set_property(GLOBAL PROPERTY USE_FOLDERS ON)

#set(EXECUTABLE_OUTPUT_PATH ${CMAKE_BINARY_DIR}/bin)
#set(LIBRARY_OUTPUT_PATH ${CMAKE_BINARY_DIR}/bin)

add_subdirectory(wrapper)
add_subdirectory(freerdp)

# Summary
message(STATUS "Configuration summary")
message(STATUS "Project name : ${PROJECT_NAME}")
message(STATUS "Project version : ${PROJECT_VERSION}")
