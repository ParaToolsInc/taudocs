Compiling
=========

Source-based instrumentation with TAU measurement code requires
compilation. At compile time, the TAU system provides several options
and configuration alternatives. This chapter explains compilation
options to enable profiling or tracing.

TAU Stub Makefile
=================

TAU configuration generates a Makefile stub as well as a library. The
Makefile name has the form

::

    Makefile.tau-<options>.
        

the library name the form

::

    libtau-<options>.a.
        

For example,

::

    %./configure -TRACE -c++=KCC -arc=sgin32
        

generates

::

    Makefile.tau-trace-kcc libtau-trace-kcc.a
    in tau-2.x/sgin32/lib
        

Using different configuration options, several modular libraries can be
built and co-exist even in the same architecture. To choose a particular
version of the library, the corresponding Makefile stub must be included
in the application Makefile. The stub Makefile defines the following
variables:

-  ``TAU_CXX`` - for the C++ compiler

-  ``TAU_CC`` - for the C compiler

-  ``TAU_F90`` - for the F90 compiler

-  ``TAU_LINKER`` - for the Linker

-  ``TAU_INCLUDE`` - for the include directories

-  ``TAU_DEFS`` - for the defines on the command-line

-  ``TAU_LIBS`` - for the TAU static library

-  ``TAU_SHLIBS`` - for the TAU shared object (dynamic library)

-  ``TAU_MPI_INCLUDE`` - for the directory where MPI header files reside

-  ``TAU_MPI_LIBS`` - for the TAU MPI library with the MPI libraries for
   C/C++

-  ``TAU_MPI_FLIBS`` - for the TAU MPI library with MPI libraries for
   Fortran

-  ``TAU_FORTRANLIBS`` - for additional fortran libraries for linking
   with C++

-  ``TAU_CXXLIBS`` - for linking with C++ libraries when native f90
   linker is used

-  ``TAU_TRACE_INPUT_LIB`` - for linking with the TAU trace reader
   library to process binary TAU traces (typically used for making a
   trace converter)

-  ``TAU_DISABLE`` - for the default TAU stub library for Fortran

-  ``TAU_USER_OPT`` - for any user defined options specified during
   configuration

In addition to these options, the stub makefile also contains
information about other packages configured with TAU. The stub makefile
defines the following variables:

-  ``PDTDIR`` - for the location of the PDT root directory

-  ``OPARIDIR`` - for the location of the Opari root directory

-  ``TULIPDIR`` - for the location of the Tulip root directory

-  ``PCLDIR`` - for the location of the PCL root directory

-  ``PAPIDIR`` - for the location of the PAPI root directory

-  ``EPILOGER`` - for the location of the EPILOG root directory

-  ``JDKDIR`` - for the location of the JDK root directory

-  ``DYNINSTDIR`` - for the location of the DyninstAPI root directory

It should be noted that the TAU library is written in C++. It may be
linked with a Fortran or a C object file in two ways. Either the
TAU\_LINKER (typically C++ compiler) may be used or the native linker
(C, F90 compiler) may be used. For Fortran programs that use the C++
linker, the ``TAU_FORTRANLIBS`` macro contains additional Fortran
libraries that need to be linked in to create the executable. If the F90
linker is used, ``TAU_CXXLIBS`` should be added to the link line which
links in the necessary C++ libraries.

A typical makefile that uses these Makefile variables is shown below:

``TAUROOTDIR`` = /usr/local/packages/tau-2.x

::

    include $(TAUROOTDIR)/sgin32/lib/Makefile.tau-trace-kcc
    CXX             = $(TAU_CXX)
    CC              = $(TAU_CC)
    CFLAGS          = $(TAU_INCLUDE) $(TAU_DEFS)
    LIBS            = $(TAU_LIBS) -lm
    LDFLAGS         = $(USER_OPT)

    RM              = /bin/rm -f
    TARGET          = matrix
    ##############################################
    all:            $(TARGET)
    install:        $(TARGET)                    
    $(TARGET):      $(TARGET).o
          $(CXX) $(LDFLAGS) $(TARGET).o -o $@ $(LIBS)
    $(TARGET).o : $(TARGET).cpp
          $(CXX) $(CFLAGS) -c $(TARGET).cpp
    clean:
            $(RM) $(TARGET).o $(TARGET)
    ##############################################
        

To use a different configuration, simply change the included makefile to
some other. For example, for

::

    % ./configure -pthread -arch=sgi64 
        

substitute

::

    include $(TAUROOTDIR)/sgi64/lib/Makefile.tau-pthread
        

in the makefile above. Also,

::

    $(TAUROOTDIR)/include/Makefile
        

points to the most recently configured version of the library.

Enabling and Disabling the Instrumentation
==========================================

Using the TAU stub makefile variable ``TAU_DEFS`` while compiling C++
and C source code enables profiling (or tracing) instrumentation and
generates the performance data files. To disable the instrumentation,
``TAU_DEFS`` should not be used. In its absence, all the TAU profiling
macros defined in the source code for instrumentation purposes are
automatically defined to null (the default behavior). Thus, the
instrumentation can be retained in the source code, since it has no
overhead when it is disabled. For Fortran however, the instrumentation
can be disabled in the program by using the TAU stub makefile variable
``TAU_DISABLE`` on the link command line. This points to a library that
contains empty TAU instrumentation routines.

Using TAU with MPI
==================

TAU MPI wrapper library (libTauMpi.a) uses the MPI Profiling Interface
for instrumentation. To use the library,

1. Configure TAU with -mpiinc=<dir> and -mpilib=<dir> command-line
   options that specify the location of MPI header files and the
   directory where MPI libraries reside. Example:

   ::

       % ./configure -mpiinc=/usr/local/packages/mpich/include \
            -mpilib=/usr/local/packages/mpich/lib/LINUX/ch_pp4 \
            -c++=KCC -cc=cc 

2. Include the TAU stub Makefile generated in the application makefile.

   ::

       TAUROOTDIR=/usr/local/packages/tau2
       include $(TAUROOTDIR)/i386_linux/Makefile.tau-kcc 
             

3. Use the Makefile variables

   ::

       $(TAU_MPI_LIBS)

   for C/C++ applications and

   ::

       $(TAU_MPI_FLIBS)

   for Fortran 90 applications, to specify the TAU MPI libraries before
   the

   ::

       $(TAU_LIBS)

   in the link command line. Also, use

   ::

       $(TAU_MPI_INCLUDE)

   in the compiler command line to specifies the MPI include directory
   to be used. Example:

   ::

       CXX     = $(TAU_CXX)
       CFLAGS  = $(TAU_INCLUDE) $(TAU_DEFS) $(TAU_MPI_INCLUDE)
       LIBS    = $(TAU_MPI_LIBS) $(TAU_LIBS)
             

4. Compile and run the MPI application as usual to generate the
   performance data.

Environment Variables
=====================

When the program has been compiled, it can be executed as it normally
would be (for example, using mpirun for an MPI task). TAU generates
profile data files or trace files in the current working directory. One
file for each context and thread is generated. To better manage
different experiments, set the environment variables

-  ``PROFILEDIR`` - to name the directory that should contain the
   profile data files and

-  ``TRACEDIR`` - the directory where event traces should be stored.

-  ``LD_LIBRARY_PATH`` - (or LIBPATH for IBM) should include the
   <tauroot>/<tauarch>/lib directory if TAU is used with JAVA 2 (using
   the -jdk=<dir> configuration option) or dyninstAPI (using the
   -dyninst=<dir> configuration option).

Example:

::

    % make 
    % setenv TRACEDIR /users/foo/tracedata/experiment1
    % mpirun -np 4 matrix
        

*Note:* TAU also uses the environment variable ``PCL_EVENT`` and
``PAPI_EVENT`` to specify the hardware performance counter to be used
when -pcl=<dir> or -papi=<dir> configuration options are used,
respectively. See ? for further details.

Application Scenarios
=====================

The TAU ``examples`` directory contains programs that illustrate the use
of TAU instrumentation and measurement options.

-  ``instrument`` - This contains a simple C++ example that shows how
   TAU API can be used for manually instrumenting a C++ program.

-  ``threads`` A simple multi-threaded program that shows how the main
   function of a thread is instrumented. Performance data is generated
   for each thread of execution. Uses pthread library and TAU must be
   configured with the ``-pthread`` option.

-  ``cthreads`` Same as threads above, but for a C program. An
   instrumented C program may be compiled with a C compiler, but needs
   to be linked with a C++ linker.

-  ``sproc`` SGI sproc threads example. TAU should be configured with
   the ``-sproc`` option to use this.

-  ``pi`` An MPI program that calculates the value of pi and e. It
   highlights the use of TAU's MPI wrapper library. TAU needs to be
   configured with -mpiinc=<dir> and -mpilib=<dir> to use this.

-  ``mpishlib`` Demonstrates the use of MPI wrapper library in
   instrumenting a shared object. The MPI application is instrumented is
   instrumented as well. TAU needs to be configured with -mpiinc=<dir>
   and mpilib=<dir> flags.

-  ``python`` Instrumentation of a python application can be done
   automatically or manually using the TAU Python bindings. Two
   examples, ``auto.py`` and ``manual.py`` demonstrate this
   respectively. TAU needs to be con-figured with-pythoninc=<dir that
   contains Python.h> option and the user needs to set ``PYTHONPATH`` to
   <taudir>/<arch>/lib to use this feature.

-  ``traceinput`` - To build a trace converter/trace reader application,
   we provide the TAU trace input library. This directory contains two
   examples (in c and c++ subdirectories) that illustrate how an
   application can use the trace input API to read online or post-mortem
   TAU binary traces. It shows how the user can register routines with
   the callback interface and how TAU invokes these routines when events
   take place.

-  ``papi`` - A matrix multiply example that shows how to use TAU
   statement level timers for comparing the performance of two
   algorithms for matrix multiplication. When used with
   `PAPI <http://icl.cs.utk.edu/papi/>`__ or
   `PCL <http://www.fz-juelich.de/zam/PCL/PCLcontent.html>`__, this can
   highlight the cache behaviors of these algorithms. TAU should be
   configured with -papi=<dir> or -pcl=<dir> and the user should set
   ``PAPI_EVENT`` - or ``PCL_EVENT`` respective environment variables,
   to use this.

-  ``papithreads`` - Same as papi, except uses threads to highlight how
   hardware performance counters may be used in a multi-threaded
   application. When it is used with PAPI, TAU should be configured with
   -papi=<dir> -pthread auto-instrument Shows the use of Program
   Database Toolkit (PDT) for automating the insertion of TAU macros in
   the source code. It requires configuring TAU with the -pdt=<dir>
   option. The Makefile is modified to illustrate the use of a source to
   source translator (tau\_instrumentor).

-  ``autoinstrument`` - Shows the use of Program Database Toolkit (PDT)
   for automating the insertion of TAU macros in the source code. It
   requires configuring TAU with the -pdt=<dir> option. The Makefile is
   modified to illustrate the use of a source to source translator
   (tau\_instrumentor).

-  ``analyze `` - Shows the use of tau\_analyze, a utility that
   generates selective instrumentation lists for use with
   tau\_instrumentor based on the analysis of collected program
   information and a user defined instrumentation scenario. The
   tau\_analyze utility expands on the functionality of the tau\_reduce
   utility. TAU must be configured with -pdt=<dir> option.

-  ``reduce`` - Shows the use of tau\_reduce, a utility that can read
   profiles and a set of rules and determine which routines should not
   be instrumented (for frequently called light-weight routines). See
   ``<tau>/utils/TAU_REDUCE.README`` file for further details. It
   requires configuring TAU with -pdt=<dir> option.

-  ``cinstrument`` - Shows the use of PDT for C. Requires configuring
   TAU with -pdt=<dir> option.

-  ``mixedmode`` - This example illustrates the use of PDT,
   hand-instrumentation (for threads), MPI library instrumentation and
   TAU system call wrapper library instrumentation. Requires configuring
   TAU with -mpiinc=<dir> -mpilib=<dir> -pdt=<dir> -pthread options.

-  ``pdt_mpi`` - This directory contains C, C++ and F90 examples that
   illustrate how TAU/PDT can be used with MPI. Requires configuring TAU
   with -pdt=<dir> -mpiinc=<dir> -mpilib=<dir> options. You may also try
   this with the ``-TRACE -epilog=<dir>`` - options to use the EPI-LOG
   tracing package (from FZJ).

-  ``callpath`` - Shows the use of call-path profiling. Requires
   configuring TAU with the ``-PROFILECALLPATH`` - option. Setting the
   environment variable ``TAU_CALLPATH_DEPTH`` - changes the depth of
   the callpath recorded by TAU. The default value of this variable is
   2.

-  ``phase`` - Shows the use of phase based profiling. Requires
   configuring TAU with the -PROFILEPHASE option. See the README file in
   the phase directory for details about the API and an example.

-  ``selective`` - This example illustrates the use of PDT, and
   selective profiling using profile groups in the tau\_instrumentor.
   Requires configuring TAU with -pdt=<dir> -fortran=<...> options.

-  ``fortran & f90`` - Show how to instrument a simple Fortran 90
   program. A C++ linker needs to be used when linking the Fortran
   application.

-  ``NPB2.3`` - `The NAS Parallel Benchmark
   2.3 <http://www.nas.nasa.gov/Software/NPB/>`__ . It shows how to use
   TAU's MPI wrapper with a manually instrumented Fortran program. LU
   and SP are the two benchmarks. LU is instrumented completely, while
   only parts of the SP program are instrumented to contrast the
   coverage of routines. In both cases MPI level instrumentation is
   complete. TAU needs to be configured with -mpi-inc=<dir> and
   -mpilib=<dir> to use this.

-  ``dyninst`` - An example that shows the use of
   `DyninstAPI <http://www.dyninst.org/>`__ to insert TAU
   instrumentation. Using Dyninst, no modifications are needed and
   tau\_run, a runtime instrumentor, inserts TAU calls at routine
   transitions in the program. [This represents work in progress].

-  ``dyninstthreads`` - The above example with threads.

-  ``java/pi`` - Shows a java program for calculating the value of pi.
   It illustrates the use of the TAU JVMPI layer for instrumenting a
   Java program without any modifications to its source code, byte-code
   or the JVM. It requires a Java 2 compliant JVM and TAU needs to be
   configured with the -jdk=<dir> option to use this.

-  ``java/api`` - The same Pi program as above that illustrates the use
   of the TAU API. There are subdirectories for C, C++ and F90 to show
   the differences in instrumentation and Makefiles. TAU needs to be
   configured with the -openmp option to use this.

-  ``openmp`` - Shows how to manually instrument an OpenMP program using
   the TAU API. There are subdirectories for C, C++ and F90 to show the
   differences in instrumentation and Makefiles. TAU needs to be
   configured with the -openmp option to use this.

-  ``opari1`` - The old version of opari. This should only be used if
   there are problems with -opari.
   `Opari <http://www.fz-juelich.de/zam/kojak/opari/>`__ is an OpenMP
   directive rewriting tool that works with TAU. Configure TAU with
   -opari=<dir> option to use this. This provides detailed
   instrumentation of OpenMP constructs. There are subdirectories for
   C++, pdt\_f90, and OpenMPI to demonstrate the use of this tool. The
   pdt\_f90 directory contains an example that shows the use of PDT with
   Opari for a Fortran 90 program.

-  ``opari`` - `Opari2 <http://www.vi-hps.org/projects/score-p/>`__ is
   an OpenMP directive rewriting tool that works with TAU. Configure TAU
   with -opari=<dir> option to use this. This provides detailed
   instrumentation of OpenMP constructs. There are subdirectories for
   C++, pdt\_f90, and OpenMPI to demonstrate the use of this tool. The
   pdt\_f90 directory contains an example that shows the use of PDT with
   Opari for a Fortran 90 program.

-  ``openmpi`` - Illustrates TAU's support for hybrid execution models
   in the form of MPI for message passing and OpenMP threads. TAU needs
   to be configured with -mpiinc=<dir> -mpilib=<dir> -openmp options to
   use this. Fork Illustrates how to register a forked process with TAU.
   TAU provides two options: ``TAU_INCLUDE_PARENT_DATA`` - and
   ``TAU_EXCLUDE_PARENT_DATA`` - which allows the child process to
   inherit or clear the performance data when the fork takes place.

-  ``fork`` - Illustrates how to register a forked process with TAU. TAU
   provides two options: ``TAU_INCLUDE_PARENT_DATA`` and
   ``TAU_EXCLUDE_PARENT_DATA`` which allows the child process to inherit
   or clear the performance data when the fork takes place.

-  ``mapping`` - Illustrates two examples in the embedded and external
   subdirectories. These correspond to profiling at the object level,
   where the time spent in a method is displayed for a specific object.
   There are two ways to achieve this using an embedded association. The
   first method requires an extension of the class definition with a TAU
   pointer and the second scheme uses external hash-table lookup that
   relies on looking at the object address at each method invocation.
   Both of these examples illustrate the use of the TAU Mapping API.

-  ``multicounters`` - Illustrates the use of multiple measurement
   options configured simultaneously in TAU. See README file for
   instructions on setting the environment variables ``COUNTERS<1-25>``
   - for specifying measurements. Requires configuring TAU with
   ``-MULTIPLECOUNTERS.``

-  ``selectiveAccess`` - Illustrates the use of TAU API for runtime
   access of TAU performance data. A program can get information about
   routines executing in its context. This can be used in conjunction
   with multiple counters.

-  ``memory`` - TAU can sample memory utilization on some platforms
   using the getrusage() system call and interrupts. This directory
   illustrates how sampling can be used to track the maximum resident
   set size. See the README file in the memory directory for further
   information.

-  ``malloc`` - TAU's malloc and free wrappers can help pinpoint where
   the memory was allocated/deallocated in a C/C++ program. It can show
   the size of memory malloc'ed and freed along with the source file
   name and line number.

-  ``taucompiler`` - using ``$(TAU_COMPILER)`` in your Makefile before
   the compiler name invokes tau\_compiler.sh - a shell script that
   instruments and compiles the source file and links in the correct
   libraries. A Fortran 90 example illustrates its use in the f90
   subdirectory.

-  ``userevent`` - TAU's user defined events can show context
   information highlighting the call-path that led to the event. This is
   supported using the ``TAU_REGISTER_CONTEXT_EVENT`` and
   ``TAU_CONTEXT_EVENT`` calls. It uses the ``TAU_CALLPATH_DEPTH``
   environment variable. This feature works independently of the
   call-path or phase profiling options, which apply to bracketed entry
   and exit events - not atomic events. You can disable tracking the
   call-path at runtime.

-  ``headroom`` - TAU's memory headroom evaluation options are discussed
   at length in the examples/headroom/README file. The amount of heap
   memory that can be allocated at any given point in the program's
   execution are tracked in this directory (and three subdirectories -
   track, here, and available). ``-PROFILEHEADROOM`` configuration
   option may be used with these examples.

-  ``mpitrace`` - Kojak's Expert tool needs traces that record events
   that call MPI routines. We track this information at runtime when TAU
   is configured with the ``-MPITRACE`` option. This example illustrates
   its use.
