//
// Copyright (c) 2016-2017, Facebook, Inc.
// Copyright (c) 2021, Neal Gompa
// All rights reserved.
//
// This source code is licensed under the Mozilla Public License, version 2.0.
// For details, see the LICENSE file in the root directory of this source tree.
// Portions of this code was previously licensed under a BSD-style license.
// See the LICENSE-BSD file in the root directory of this source tree for details.

#include <APPX/XML.h>
#include <unordered_map>

namespace osinside {
namespace appx {
    std::string XMLEncodeString(const std::string &s)
    {
        static const std::unordered_map<char, const char *> sEncodeMap = {
            {'"', "&quot;"}, {'&', "&amp;"}, {'\'', "&apos;"},
            {'<', "&lt;"},   {'>', "&gt;"},
        };

        std::string encoded;
        encoded.reserve(s.size());
        for (char c : s) {
            auto it = sEncodeMap.find(c);
            if (it != sEncodeMap.end()) {
                encoded += it->second;
            } else {
                encoded += c;
            }
        }
        return encoded;
    }
}
}
