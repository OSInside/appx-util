# appx-util

`appx` is a tool which creates and optionally signs
Microsoft Windows APPX packages.

## Supported targets

`appx` can create APPX packages for the following operating
systems:

* Windows 10 (UAP)
* Windows 10 Mobile

## Building appx

Prerequisites:

* CMake >= 3.11
* OpenSSL developer library
* zlib developer library

This tool works only on *nix based systems with GCC 7 or newer (or equivalent).
Linux is the primary target, and while macOS _may_ work, we do not commit to supporting it.

Build:

    mkdir Build && cd Build && cmake .. && make

Install:

    cd Build && make install

## Running appx

Run `appx -h` for usage information.

## Contributing

appx-util actively welcomes contributions from the community.
If you're interested in contributing, be sure to check out the
[contributing guide](https://github.com/OSInside/appx-util/blob/master/CONTRIBUTING.md).
It includes some tips for getting started in the codebase, as well
as important information about the license.
