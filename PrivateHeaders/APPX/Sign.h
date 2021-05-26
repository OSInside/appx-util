//
// Copyright (c) 2016-2017, Facebook, Inc.
// Copyright (c) 2021, Neal Gompa
// All rights reserved.
//
// This source code is licensed under the Mozilla Public License, version 2.0.
// For details, see the LICENSE file in the root directory of this source tree.
// Portions of this code was previously licensed under a BSD-style license.
// See the LICENSE-BSD file in the root directory of this source tree for details.

#pragma once

#include <APPX/Hash.h>
#include <APPX/OpenSSL.h>
#include <cstdint>
#include <openssl/pkcs7.h>

namespace osinside {
namespace appx {
    struct APPXDigests;

    // Creates a PKCS7 signature for the given APPX digest using the given
    // certificate.
    OpenSSLPtr<PKCS7, PKCS7_free> Sign(const std::string &certPath,
                                       const APPXDigests &digests);

    // A set of digests required when signing APPX files.
    struct APPXDigests
    {
        SHA256Hash axpc;  // ZIPFILERECORD-s.
        SHA256Hash axcd;  // ZIPDIRECTORYENTRY-s.
        SHA256Hash axct;  // [Content_Types].xml (uncompressed).
        SHA256Hash axbm;  // AppxBlockMap.xml (uncompressed).
        // AppxMetadata/CodeIntegrity.cat (uncompressed, optional).
        SHA256Hash axci;

        template <typename TSink>
        void Write(TSink &sink) const
        {
            static const std::uint8_t signature[] = {0x41, 0x50, 0x50, 0x58};
            sink.Write(sizeof(signature), signature);
            static const std::uint8_t axpcSignature[] = {0x41, 0x58, 0x50,
                                                         0x43};
            sink.Write(sizeof(axpcSignature), axpcSignature);
            sink.Write(sizeof(this->axpc.bytes), this->axpc.bytes);
            static const std::uint8_t axcdSignature[] = {0x41, 0x58, 0x43,
                                                         0x44};
            sink.Write(sizeof(axcdSignature), axcdSignature);
            sink.Write(sizeof(this->axcd.bytes), this->axcd.bytes);
            static const std::uint8_t axctSignature[] = {0x41, 0x58, 0x43,
                                                         0x54};
            sink.Write(sizeof(axctSignature), axctSignature);
            sink.Write(sizeof(this->axct.bytes), this->axct.bytes);
            static const std::uint8_t axbmSignature[] = {0x41, 0x58, 0x42,
                                                         0x4D};
            sink.Write(sizeof(axbmSignature), axbmSignature);
            sink.Write(sizeof(this->axbm.bytes), this->axbm.bytes);
            static const std::uint8_t axciSignature[] = {0x41, 0x58, 0x43,
                                                         0x49};
            sink.Write(sizeof(axciSignature), axciSignature);
            sink.Write(sizeof(this->axci.bytes), this->axci.bytes);
        }
    };
}
}
