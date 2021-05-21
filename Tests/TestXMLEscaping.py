#!/usr/bin/env python2.7
#
# Copyright (c) 2016-present, Facebook, Inc.
# Copyright (c) 2021, Neal Gompa
# All rights reserved.
#
# This source code is licensed under the Mozilla Public License, version 2.0.
# For details, see the LICENSE file in the root directory of this source tree.

from appx.util import appx_exe
from xml.etree import ElementTree
import appx.util
import os
import subprocess
import unittest
import zipfile

class TestXMLEscaping(unittest.TestCase):
    '''
    Ensures the appx tool escapes XML correctly.
    '''

    def test_xml_encoding(self):
        with appx.util.temp_dir() as d:
            filename = "hello&world'@!#$%^txt"
            file_path = os.path.join(d, filename)
            with open(file_path, 'w') as readme:
                pass
            subprocess.check_call([appx_exe(),
                                   '-o', os.path.join(d, 'test.appx'),
                                   '-c', appx.util.test_key_path(),
                                   file_path])
            with zipfile.ZipFile(os.path.join(d, 'test.appx')) as zip:
                block_map_text = zip.read('AppxBlockMap.xml')
                block_map_xml = ElementTree.fromstring(block_map_text)
                block_map_filename = block_map_xml[0].get('Name')
                self.assertEqual(filename, block_map_filename)

                # In an ideal world, the AppxBlockMap validating as XML
                # and containing the correctly escaped filename would be
                # a sufficient test. However, Microsoft's appx parser
                # appears to choke on additional XML escapes, so make
                # sure we only escaped the characters we were expecting
                # to escape.
                escaped = filename.replace('&', '&amp;')
                escaped = escaped.replace("'", '&apos;')
                self.assertIn(escaped, block_map_text)

if __name__ == '__main__':
    unittest.main()
