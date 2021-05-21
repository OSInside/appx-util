#
# Copyright (c) 2016-2017, Facebook, Inc.
# Copyright (c) 2021, Neal Gompa
# All rights reserved.
#
# This source code is licensed under the Mozilla Public License, version 2.0.
# For details, see the LICENSE file in the root directory of this source tree.

cmake_minimum_required(VERSION 3.11)
enable_testing()

project(appx CXX)

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

# OpenSSL is deprecated on OS X.
function (APPX_CHECK_OPENSSL_WITH_FLAGS NAME FLAGS)
  set(CMAKE_REQUIRED_FLAGS "${FLAGS}")
  set(CMAKE_REQUIRED_INCLUDES ${OPENSSL_INCLUDE_DIRS})
  set(CMAKE_REQUIRED_LIBRARIES ${OPENSSL_LIBRARIES})
  check_cxx_source_compiles("#include <openssl/asn1.h>

                             int
                             main()
                             {
                               ASN1_STRING *s = ASN1_STRING_new();
                               ASN1_STRING_free(s);
                               return 0;
                             }
                             "
                             "${NAME}"
                             FAIL_REGEX "is deprecated")
endfunction ()
appx_check_openssl_with_flags(APPX_HAS_UNDEPRECATED_OPENSSL "")
if (NOT APPX_HAS_UNDEPRECATED_OPENSSL)
  appx_check_openssl_with_flags(APPX_HAS_SUPPRESSABLE_DEPRECATED_OPENSSL
                                -Wno-deprecated-declarations)
  if (APPX_HAS_SUPPRESSABLE_DEPRECATED_OPENSSL)
    set_property(TARGET appx
                 APPEND PROPERTY COMPILE_OPTIONS -Wno-deprecated-declarations)
  endif ()
endif ()

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
