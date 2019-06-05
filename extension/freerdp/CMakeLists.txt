# Minimum CMake required
cmake_minimum_required(VERSION 3.10)

include(${CMAKE_ROOT}/Modules/ExternalProject.cmake)

ExternalProject_Add(
  FreeRDP
  GIT_REPOSITORY "https://github.com/FreeRDP/FreeRDP"
  GIT_TAG "2.0.0-rc4"
  CMAKE_ARGS -DCMAKE_INSTALL_PREFIX=${CMAKE_CURRENT_BINARY_DIR}/FreeRDP
)

add_library(libfreerdp STATIC IMPORTED GLOBAL)
add_dependencies(libfreerdp FreeRDP)

set(LIBFREERDP_INCLUDE_DIR ${CMAKE_CURRENT_BINARY_DIR}/FreeRDP/include/freerdp2 ${CMAKE_CURRENT_BINARY_DIR}/FreeRDP/include/winpr2)
set(LIBFREERDP_LIB ${CMAKE_CURRENT_BINARY_DIR}/FreeRDP/lib/libfreerdp2.so)
file(MAKE_DIRECTORY ${LIBFREERDP_INCLUDE_DIR})
set_target_properties(libfreerdp PROPERTIES
	INTERFACE_INCLUDE_DIRECTORIES "${LIBFREERDP_INCLUDE_DIR}"
	IMPORTED_LOCATION "${LIBFREERDP_LIB}"
)

