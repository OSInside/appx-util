#!/usr/bin/env python3
#
# Copyright (c) 2016-present, Facebook, Inc.
# Copyright (c) 2021, Neal Gompa
# All rights reserved.
#
# This source code is licensed under the Mozilla Public License, version 2.0.
# For details, see the LICENSE file in the root directory of this source tree.
# Portions of this code was previously licensed under a BSD-style license.
# See the LICENSE-BSD file in the root directory of this source tree for details.

from appx.util import appx_exe
import appx.util
import errno
import os
import subprocess
import unittest
import zipfile

class TestInputs(unittest.TestCase):
    '''
    Ensures the appx tool creates ZIP files with the correct files inside.
    '''

    def test_flat_files(self):
        with appx.util.temp_dir() as d:
            with open(os.path.join(d, 'README.txt'), 'wb') as readme:
                readme.write(b'This is a test file.\n')
            os.mkdir(os.path.join(d, 'somedir'))
            with open(os.path.join(d, 'somedir', 'other_file.dll'), 'wb') \
                as other_file:
                other_file.write(b'MZ')
            subprocess.check_call([
                appx_exe(), '-o', os.path.join(d, 'test.appx'),
                os.path.join(d, 'README.txt'),
                os.path.join(d, 'somedir', 'other_file.dll')])
            with zipfile.ZipFile(os.path.join(d, 'test.appx')) as zip:
                self.assertIn('README.txt', zip.namelist())
                self.assertIn('other_file.dll', zip.namelist())
                self.assertNotIn('somedir/other_file.dll', zip.namelist())

    def test_directory(self):
        with appx.util.temp_dir() as d:
            with open(os.path.join(d, 'README.txt'), 'wb') as readme:
                readme.write(b'This is a test file.\n')
            os.mkdir(os.path.join(d, 'somedir'))
            with open(os.path.join(d, 'somedir', 'other_file.dll'), 'wb') \
                as other_file:
                other_file.write(b'MZ')
            subprocess.check_call([appx_exe(), '-o',
                                   os.path.join(d, 'test.appx'), d])
            with zipfile.ZipFile(os.path.join(d, 'test.appx')) as zip:
                self.assertIn('README.txt', zip.namelist())
                self.assertIn('somedir/other_file.dll', zip.namelist())
                self.assertNotIn('somedir', zip.namelist())
                self.assertNotIn('somedir/', zip.namelist())
                self.assertNotIn('test.appx', zip.namelist())

    def test_file_mapping(self):
        with appx.util.temp_dir() as d:
            with open(os.path.join(d, 'README.txt'), 'wb') as readme:
                readme.write(b'This is a test file.\n')
            with open(os.path.join(d, 'other_file.dll'), 'wb') as other_file:
                other_file.write(b'MZ')
            subprocess.check_call([
                appx_exe(), '-o', os.path.join(d, 'test.appx'),
                'README.txt={}'.format(os.path.join(d, 'README.txt')),
                'somedir/other_file.dll={}'.format(
                    os.path.join(d, 'other_file.dll')),
                ])
            with zipfile.ZipFile(os.path.join(d, 'test.appx')) as zip:
                self.assertIn('README.txt', zip.namelist())
                self.assertNotIn('other_file.dll', zip.namelist())
                self.assertIn('somedir/other_file.dll', zip.namelist())

    def test_mapping_file(self):
        with appx.util.temp_dir() as d:
            with open(os.path.join(d, 'README.txt'), 'wb') as readme:
                readme.write(b'This is a test file.\n')
            with open(os.path.join(d, 'other_file.dll'), 'wb') as other_file:
                other_file.write(b'MZ')
            with open(os.path.join(d, 'mapping.txt'), 'w') as mapping_file:
                mapping_file.write(
                    '[Files]\n'
                    '"{}" "README.txt"\n'
                    '"{}" "somedir/other_file.dll"\n'.format(
                        self.__quote_mapping_file_path(
                            os.path.join(d, 'README.txt')),
                        self.__quote_mapping_file_path(
                            os.path.join(d, 'other_file.dll'))))
            subprocess.check_call([
                appx_exe(), '-o', os.path.join(d, 'test.appx'),
                '-f', os.path.join(d, 'mapping.txt'),
            ])
            with zipfile.ZipFile(os.path.join(d, 'test.appx')) as zip:
                self.assertIn('README.txt', zip.namelist())
                self.assertNotIn('other_file.dll', zip.namelist())
                self.assertIn('somedir/other_file.dll', zip.namelist())

    def test_mapping_file_missing(self):
        with appx.util.temp_dir() as d:
            process = subprocess.Popen([
                appx_exe(), '-o', os.path.join(d, 'test.appx'),
                '-f', os.path.join(d, 'mapping.txt'),
            ], stderr=subprocess.PIPE)
            (_, stderr) = process.communicate()
            self.assertEqual(1, process.returncode)
            self.assertNotIn('Malformed', stderr.decode('utf-8'))
            # TODO(strager)
            #self.assertIn('mapping.txt', stderr)
            #self.assertIn('no such file', stderr)

    def test_mapping_file_syntax(self):
        with appx.util.temp_dir() as d:
            with open(os.path.join(d, 'README.txt'), 'wb') as readme:
                readme.write(b'This is a test file.\n')
            mapping_file_test_cases = [
                # One file.
                '[Files]\n"{}" "README.txt"'.format(
                    self.__quote_mapping_file_path(
                        os.path.join(d, 'README.txt'))),
                '[Files]\n"{}" "README.txt"\n'.format(
                    self.__quote_mapping_file_path(
                        os.path.join(d, 'README.txt'))),

                # Empty lines.
                (
                    '\n'
                    '[Files]\n'
                    '\n'
                    '\n'
                    '"{}" "README.txt"\n'
                    '\n'.format(self.__quote_mapping_file_path(
                        os.path.join(d, 'README.txt')))),

                # Whitespace.
                (
                    ' \n'
                    '[Files]\n'
                    ' \t\n'
                    '   \n'
                    ' "{}" "README.txt"\t\n'
                    ' \n'.format(self.__quote_mapping_file_path(
                        os.path.join(d, 'README.txt')))),
            ]
            for mapping_file_test_case in mapping_file_test_cases:
                with open(os.path.join(d, 'mapping.txt'), 'w') as mapping_file:
                    mapping_file.write(mapping_file_test_case)
                try:
                    os.remove(os.path.join(d, 'test.appx'))
                except OSError as e:
                    if e.errno == errno.ENOENT:
                        # Ignore.
                        pass
                    else:
                        raise
                subprocess.check_call([
                    appx_exe(), '-o', os.path.join(d, 'test.appx'),
                    '-f', os.path.join(d, 'mapping.txt'),
                ])
                with zipfile.ZipFile(os.path.join(d, 'test.appx')) as zip:
                    self.assertIn('README.txt', zip.namelist())

    def test_mapping_file_corrupt_syntax(self):
        with appx.util.temp_dir() as d:
            mapping_file_test_cases = [
                '[Files',
                '[Files]\n"',
                '[Files]\n"{}" "README.txt" ""\n'.format(
                    self.__quote_mapping_file_path(
                        os.path.join(d, 'README.txt'))),
            ]
            for mapping_file_test_case in mapping_file_test_cases:
                with open(os.path.join(d, 'mapping.txt'), 'w') as mapping_file:
                    mapping_file.write(mapping_file_test_case)
                try:
                    os.remove(os.path.join(d, 'test.appx'))
                except OSError as e:
                    if e.errno == errno.ENOENT:
                        # Ignore.
                        pass
                    else:
                        raise
                process = subprocess.Popen([
                    appx_exe(), '-o', os.path.join(d, 'test.appx'),
                    '-f', os.path.join(d, 'mapping.txt'),
                ], stderr=subprocess.PIPE)
                (_, stderr) = process.communicate()
                self.assertEqual(1, process.returncode)
                self.assertIn('mapping.txt', stderr.decode('utf-8'))
                self.assertIn('Malformed', stderr.decode('utf-8'))

    def test_mapping_file_stdin(self):
        with appx.util.temp_dir() as d:
            with open(os.path.join(d, 'README.txt'), 'wb') as readme:
                readme.write(b'This is a test file.\n')
            with open(os.path.join(d, 'other_file.dll'), 'wb') as other_file:
                other_file.write(b'MZ')
            mapping_file = (
                '[Files]\n'
                '"{}" "README.txt"\n'
                '"{}" "somedir/other_file.dll"\n'.format(
                    self.__quote_mapping_file_path(
                        os.path.join(d, 'README.txt')),
                    self.__quote_mapping_file_path(
                        os.path.join(d, 'other_file.dll'))))
            command = [
                appx_exe(), '-o', os.path.join(d, 'test.appx'),
                '-f', '-',
            ]
            process = subprocess.Popen(command, stdin=subprocess.PIPE)
            (_, _) = process.communicate(mapping_file.encode('utf-8'))
            if process.returncode != 0:
                raise subprocess.CalledProcessError(process.returncode, command)
            with zipfile.ZipFile(os.path.join(d, 'test.appx')) as zip:
                self.assertIn('README.txt', zip.namelist())
                self.assertNotIn('other_file.dll', zip.namelist())
                self.assertIn('somedir/other_file.dll', zip.namelist())

    @staticmethod
    def __quote_mapping_file_path(path):
        # TODO(strager): Escape '"'.
        return path

if __name__ == '__main__':
    unittest.main()
