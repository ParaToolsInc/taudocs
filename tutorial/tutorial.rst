TAU Tutorial
============

Gather information
==================

Before we began installing PDT and TAU you will find it helpful to
gather information about your computing environment. TAU and PDT require
both a C and C++ compiler. Furthermore this tutorial uses MPICH, if you
use a different implementation just find its lib and include
directories. Find out the following information about your computing
environment before we began:

-  The path to your MPI lib directory

-  The path to your MPI include directory

-  The path of your C compiler (same as the used to compile MPI)

-  The path of your C++ compiler (same as the used to compile MPI)

For the remaining of this tutorial we will assume that your C compiler
is xlc, your C++ compiler is xlC.

Installing PDT
==============

To take advantage of TAU's automatic instrumentation features, you will
need to install the Program Database Toolkit (PDT). Download the latest
version from the PDT pages and put the tar.gz package in the location
that you want to install PDT. For this installation, we will assume that
you are using IBM's Fortran and C/C++ compilers, with an mpich
installation.

Start by uncompressing the PDT package and moving into the PDT
directory.

::

    %> tar -xvzf pdtoolkit-x.x.tar.gz
    %> cd pdtoolkit

You can get a sense for what options you can configure PDT with by
entering:

::

    %> ./configure
    Program Database Toolkit (PDT) Configuration
    --------------------------------------------
    Looks like a Linux machine ...
    Looking for C++ compilers .... done
    Usage: ./configure [-GNU|-CC|-c++|-cxx|-xlC|-pgCC|-icpc|-ecpc]
                       [-arch=ibm64|ibm64linux|IRIXO32|IRIXN32|IRIX64] [-help]
                       [-compdir=<compdir>>]
                       [-enable-old-headers]
                       [-useropt=<options>>]
                       [-prefix=<dir>]
                       [-exec-prefix=<dir>>]

We will configure PDT for use the the Fortran xlF, xlc, and xlC
compilers. To configure PDT, type

::

    %> ./configure -xlC

    Program Database Toolkit (PDT) Configuration
    --------------------------------------------
    Looks like a Linux machine ...
    Looking for C++ compilers .... done
    ==> Using /opt/ibmcmp/vacpp/6.0/bin/xlC
    Unpacking ppc64/bin ...
    ==> ARCH is PPCLINUX
    ==> PLATFORM is ppc64
    ==> Default compiler options are -O2
    ==> Makefiles were configured
    ==> cparse was configured
    ==> cxxparse was configured
    ==> f90parse was configured
    ==> f95parse was configured

    Configuration is complete!

    Run "make" and "make install"
    Add "/home/users/hoge/pdtoolkit-3.4/ppc64//bin" to your path

Add the specified directory to your path. In bash, for example you could
enter

::

    %> export PATH=$PATH:/home/users/hoge/pdtoolkit/ppc64/bin

Now, build and install PDT. Unless you specify a different location to
install PDT, it will be placed in the current working directory.

::

    %> make
    ...
    %> make install

Now you're ready to proceed with the TAU installation.

Installing TAU
==============

Download the latest version of TAU from the TAU home. Place the
distribution In the directory that you want to install TAU. Type

::

    %> tar -xvzf tau_latest.tar.gz
    %> cd tau2

We will be installing TAU once again assuming that we are using the IBM
compilers (xlf, xlc and xlC), and an MPICH installation. Note where your
MPICH installation resides, and configure TAU by entering (replacing the
MPICH specifics with those in your local system.

::

    %> ./configure -c++=xlC -cc=xlc -fortran=ibm \
      -mpiinc=/opt/osshpc/mpich-1.2.5/32/ch_shmem/include \
      -mpilib=/opt/osshpc/mpich-1.2.5/32/ch_shmem/lib \
      -pdt=/home/users/hoge/pdtoolkit

Add the TAU directory to your path and install.

::

    %> export PATH=$PATH:/home/users/hoge/tau2/ppc64/bin
    %> make install

TAU is installed, and you're ready to start profiling your code.

Automatic instrumentation using TAU Compiler
============================================

For this section of the tutorial we will be using the files found in the
``examples/taututorial`` directory of the tau distribution. To start,
there are two files of note: computePi.cpp and Makefile. computePi.cpp
is a C++ program that uses an MPI client-server model to estimate the
value of Pi. The server accepts requests for random numbers from the
clients, and returns an array of random numbers to the clients. The
clients use these values to estimate Pi using a dart-throwing method.
When the clients have converged to a satisfactory tolerance, they signal
their completion to the server and the program exits.

Build computePi.cpp as you would any c++ mpi application.

::

    %> mpicxx -c computePi.cpp -o computePi.o
    %> mpicxx computePi.o -o computePi
        

Test the program in your MPI environment. For mpich, the command might
be

::

    %> mpirun -np 5 ./computePi
    Pi is 3.14226

to run the program on 5 nodes. Note that this program requires at least
two nodes to be running! Once you've confirmed that the program ran
successfully, try timing it to get a sense of how long it takes to run.

::

    %> time mpirun -np 5 ./computePi
    Pi is 3.14226

    real    0m2.012s
    user    0m1.570s
    sys     0m0.330s

Now let us rebuild computePi to be instrumented with tau. First we need
to tell TAU which instrumentation library to use by setting the
environment variable TAU\_MAKEFILE to the location of the tau makefile,
for example:

::

    %> export TAU_MAKEFILE=/home/users/hoge/tau2/ia64/lib/Makefile.tau-mpi-pdt
    %> tau_cxx.sh -c computePi.cpp -o computePi.o
    %> tau_cxx.sh computePi.o -o computePi

Assuming that all goes well, the computePi program will have been
automatically built with TAU instrumentation. Run the program as you
would any MPI program, i.e.

::

    %> mpirun -np 5 ./computePi
    Pi is 3.14226

TAU generates a profile file for every node the program is run on. You
can see these files by doing a directory listing.

::

    %> ls profile*
    profile.0.0.0  profile.1.0.0  profile.2.0.0  
    profile.3.0.0  profile.4.0.0

Now you're ready to view the output of TAU. If you've added the TAU
binary directory to your path you can launch the TAU profile viewer,
Paraprof.

::

    %> paraprof

Enjoy exploring the performance data displayed by Paraprof. A complete
description of how to use Paraprof is outside the scope of this
document. Please see the `Paraprof
Manual <http://www.cs.uoregon.edu/research/tau/docs/paraprof/index.html>`__
for more information.

When you ran the instrumented version of computePi you might have
noticed that it took significantly longer to run than the
non-instrumented version. Let's verify this behavior.

::

    %> time mpirun -np 5 ./computePi
    real    0m37.750s
    user    0m37.370s
    sys     0m0.320s

On my system, this is an order of magnitude overhead. For
multi-processor MPI programs, this is an unacceptable amount of
overhead. However, TAU offers a method for dealing with this added
overhead, which we'll explore that in the next section.

TAU throttle
============

Tau\_THROTTLE is designed to reduce the computational overhead
associated with instrumenting a program with TAU. This usually takes the
form of selectively instrumented some functions but not others. This can
be done manually, but TAU\_THROTTLE with do this automatically by
helping you develop a criterion to decide which function to instrument.

Looking at the #call column we see that the function computeRandom() is
called about 20,000,000 times. It is functions like these that
contribute greatly to the overhead associated with instrumenting a
program. You see, when a function is entered and exited a small amount
of tauinstrument code is executed. When a function is called millions of
times even that small amount of code can cause a slow down in execute
time.

Let us tell tau not to instrument functions like computeRandom(), this
will remove the computational overhead of instrumenting a function that
is called 20 millions times. To do this, set these environment
variables:

::

    %> export TAU_THROTTLE=1
    %> export TAU_THROTTLE_NUMCALLS=400000
    %> export TAU_THROTTLE_PERCALL=3000

This will tell tau not to profile any functions which are called more
than 400000 times and their inclusive time per call is less than 3
seconds.

Let us now see how much time it takes to run computePi,

::

    %> time mpirun -np 5 ./computePi
    Pi is 3.14226

    real    0m2.123s
    user    0m1.760s
    sys     0m0.270s

On my machine computePi runs at about 10% overhead much better than the
overhead before using TAU\_THROTTLE. Not only does TAU\_THROTTLE help
reduce the overall runtime overhead of instrumenting a program, it also,
as we will see in the next section, increases the accuracy of the
resulting profile data.

ParaProf
========

Paraprof is a tool that shows you a graphical representation of the
profiles generated by tau\_compiler. Documentation on setting up and
using paraprof is outside the scope of this tutorial, see the `ParaProf
Manual <http://www.cs.uoregon.edu/research/tau/docs/paraprof/index.html>`__

Here is the results of using TAU\_THROTTLE are displayed in paraprof.
Notice that before TAU\_THROTTLE that the number of calls made to
functions other than computeRandom() is obscured. But after
TAU\_THROTTLE they can be seen clearly.

Congratulations, you have successfully instrumented a C++ program with
tau compiler. Furthermore the you know the basics of TAU\_THROTTLE and
how it can help reduce the overhead of instrumenting a program. For more
information on tau features see the `Tau
Documentation. <http://www.cs.uoregon.edu/research/tau/docs.php>`__
