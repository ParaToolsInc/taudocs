Windows
=======

TAU on Windows
==============

Installation
------------

We provide a binary release build for Windows on the `download
page <http://www.cs.uoregon.edu/research/tau/downloads.php>`__. TAU can
also be built form source using ``Makefile.win32``.

Instrumenting an application with Visual Studio C/C++
-----------------------------------------------------

Here is a step by step guide for retrieving a standard profile from a
threaded program.

1. Download TAU (see previous section)

2. Open ``[TAU-HOME]/examples/threads/threads.sln`` in VC 7 or greater.

3. Open ``testTau.cpp`` source file.

4. Uncomment the pragma element at the top of the file so that it reads:

   ::

       #define PROFILING_ON 1
       #pragma comment(lib, "tau-profile-static-mt.lib")

5. Edit these properties of this project:

   1. Add the ``..\..\lib\vc7\`` directory to the Linker's Additional
      Library Directories.

   2. Set the Runtime Library to ``Multi-threaded DLL
                (MD)``\ in the C/C++ Code Generation section.

6. Build and run the application.

7. Launch Visual Studio's command line prompt Move to the
   ``[TAU-HOME]/examples/threads/directory/`` this is where the profile
   files where written. Type:

   ::

       %> [TAU-HOME]/bin/paraprof

   To view these profiles in pararprof

Using MINGW with TAU
--------------------

::

    Building TAU with the MinGW cross-compilers for 32- or 64-bit Windows

    Requirements:

    MinGW compilers must be in your path.  For example (64-bit):
    * x86_64-w64-mingw32-gcc
    * x86_64-w64-mingw32-g++
    * x86_64-w64-mingw32-ar
    * x86_64-w64-mingw32-ld
    * x86_64-w64-mingw32-ranlib

    Limitations:

    * No signal processing
    * No event-based sampling (EBS)

    Instructions:

    See ./configure -help.
