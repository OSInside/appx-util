//
// Copyright (c) 2016-2017, Facebook, Inc.
// Copyright (c) 2021, Neal Gompa
// All rights reserved.
//
// This source code is licensed under the Mozilla Public License, version 2.0.
// For details, see the LICENSE file in the root directory of this source tree.
// Portions of this code was previously licensed under a BSD-style license.
// See the LICENSE-BSD file in the root directory of this source tree for details.

#include <APPX/ZIP.h>
#include <cstdio>
#include <cstring>
#include <string>

namespace osinside {
namespace appx {
    std::string ZIPFileEntry::SanitizedFileName(const std::string &fileName)
    {
        static const char kWhitelist[] =
            "abcdefghijklmnopqrstuvwxyz"
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            "0123456789"
            "-._~/";
        static const char *kContentTypesFile = "[Content_Types].xml";

        // [Content_Types.xml] is a special case: the [] in the name
        // should not be escaped, otherwise the appx will be invalid
        if (fileName == kContentTypesFile) {
            return fileName;
        }

        std::string s;
        s.reserve(fileName.size());
        for (char c : fileName) {
            if (std::strchr(kWhitelist, c)) {
                s += c;
            } else {
                char buffer[4];
                int rc = std::snprintf(buffer, sizeof(buffer), "%%%02X",
                                       static_cast<unsigned char>(c));
                assert(rc == 3);
                s += buffer;
            }
        }
        return s;
    }
}
}
