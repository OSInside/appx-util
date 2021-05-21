//
// Copyright (c) 2016-2017, Facebook, Inc.
// Copyright (c) 2021, Neal Gompa
// All rights reserved.
//
// This source code is licensed under the Mozilla Public License, version 2.0.
// For details, see the LICENSE file in the root directory of this source tree.

#include <APPX/File.h>

namespace facebook {
namespace appx {
    ErrnoException::ErrnoException() : ErrnoException(errno)
    {
    }

    ErrnoException::ErrnoException(const std::string &message)
        : ErrnoException(message, errno)
    {
    }

    ErrnoException::ErrnoException(int error)
        :  // Avoid allocations by using the const char * overload of
          // std::runtime_error.
          std::runtime_error(std::strerror(error)),
          error(error)
    {
    }

    ErrnoException::ErrnoException(const std::string &message, int error)
        : std::runtime_error(std::strerror(error) + std::string(": ") +
                             message),
          error(error)
    {
    }
}
}
