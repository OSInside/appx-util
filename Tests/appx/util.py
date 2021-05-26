#
# Copyright (c) 2016-2017, Facebook, Inc.
# Copyright (c) 2021, Neal Gompa
# All rights reserved.
#
# This source code is licensed under the Mozilla Public License, version 2.0.
# For details, see the LICENSE file in the root directory of this source tree.
# Portions of this code was previously licensed under a BSD-style license.
# See the LICENSE-BSD file in the root directory of this source tree for details.

import contextlib
import os
import shutil
import tempfile

@contextlib.contextmanager
def temp_dir():
    dir = tempfile.mkdtemp()
    try:
        yield dir
    finally:
        shutil.rmtree(dir)

def appx_exe():
    path = os.getenv('APPX_EXE_PATH')
    if path is None:
        raise Exception('APPX_EXE_PATH environment variable must be specified')
    return path

def test_dir_path():
    return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

def test_key_path():
    return os.path.join(test_dir_path(), 'App_TemporaryKey.pfx')
