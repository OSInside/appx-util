//
// Copyright (c) 2016-2017, Facebook, Inc.
// Copyright (c) 2021, Neal Gompa
// All rights reserved.
//
// This source code is licensed under the Mozilla Public License, version 2.0.
// For details, see the LICENSE file in the root directory of this source tree.

#pragma once

#include <APPX/File.h>
#include <string>
#include <unordered_map>
#include <zlib.h>

namespace facebook {
namespace appx {
    // Creates and optionally signs an APPX file.
    //
    // fileNames maps APPX archive names to local filesystem paths.
    //
    // certPath, if specified, causes the APPX to be signed. certPath points to
    // the path to the PKCS12 certificate file containing the private signing
    // key.
    //
    // compressionLevel indicates how much to compress individual files.
    // Z_DEFAULT_COMPRESSION and any value between Z_NO_COMPRESSION and
    // Z_BEST_COMPRESSION are accepted.
    void WriteAppx(
        const FilePtr &zip,
        const std::unordered_map<std::string, std::string> &fileNames,
        const std::string *certPath, int compressionLevel, bool bundle);
}
}
