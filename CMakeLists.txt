#
# Copyright (c) 2016-2017, Facebook, Inc.
# Copyright (c) 2021, Neal Gompa
# All rights reserved.
#
# This source code is licensed under the Mozilla Public License, version 2.0.
# For details, see the LICENSE file in the root directory of this source tree.
# Portions of this code was previously licensed under a BSD-style license.
# See the LICENSE-BSD file in the root directory of this source tree for details.

cmake_minimum_required(VERSION 3.11)
enable_testing()

project(appx
        VERSION 0.3
        LANGUAGES CXX)

include(CheckCXXSourceCompiles)
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
find_package(OpenSSL REQUIRED)
find_package(ZLIB REQUIRED)

add_executable(appx
               Sources/APPX.cpp
               Sources/File.cpp
               Sources/OpenSSL.cpp
               Sources/Sign.cpp
               Sources/XML.cpp
               Sources/ZIP.cpp
               Sources/main.cpp)
target_include_directories(appx
                           PRIVATE
                           PrivateHeaders
                           ${OPENSSL_INCLUDE_DIR}
                           ${ZLIB_INCLUDE_DIRS})
target_link_libraries(appx
                      PRIVATE
                      ${OPENSSL_LIBRARIES}
                      ${ZLIB_LIBRARIES})
install(TARGETS appx RUNTIME DESTINATION bin)

function (APPX_ADD_TEST NAME)
  add_test(NAME "${NAME}"
           COMMAND "${CMAKE_CURRENT_SOURCE_DIR}/Tests/${NAME}.py")
  set_property(TEST "${NAME}" PROPERTY
               ENVIRONMENT "APPX_EXE_PATH=$<TARGET_FILE:appx>")
endfunction ()
appx_add_test(TestInputs)
appx_add_test(TestValidZIP)
appx_add_test(TestXMLEscaping)
appx_add_test(TestZIPEscaping)
appx_add_test(TestContentTypes)
appx_add_test(TestEmptyFile)
