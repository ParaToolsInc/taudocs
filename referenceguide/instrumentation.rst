TAU Instrumentation Options
===========================

Selective Instrumentation Options
=================================

``BEGIN_EXCLUDE_LIST`` / ``END_EXCLUDE_LIST`` or ``BEGIN_INCLUDE_LIST``
/ ``END_INCLUDE_LIST``
    exclude/include list of routines and/or files for instrumentation.
    The list of routines to be excluded from instrumentation is
    specified, one per line, enclosed by ``BEGIN_EXCLUDE_LIST`` and
    ``END_EXCLUDE_LIST``. Instead of specifying which routines should be
    excluded, the user can specify the list of routines that are to be
    instrumented using the include list, one routine name per line,
    enclosed by ``BEGIN_INCLUDE_LIST`` and ``END_INCLUDE_LIST``.

``BEGIN_FILE_EXCLUDE_LIST`` / ``END_FILE_EXCLUDE_LIST`` or
``BEGIN_FILE_INCLUDE_LIST`` / ``END_FILE_INCLUDE_LIST``
    Similarly, files can be included or excluded with the
    ``BEGIN_FILE_EXCLUDE_LIST, END_FILE_EXCLUDE_LIST,
                BEGIN_FILE_INCLUDE_LIST, and END_FILE_INCLUDE_LIST ``
    lines.

``BEGIN_INSTRUMENT_SECTION`` / ``END_INSTRUMENT_SECTION``
    Manually editing the selective instrumentation file gives you more
    options. These tags allow you to control the type of instrumentation
    performed in certain portions of your application.

-  Static and Dynamic timers can be set by specifying either a range of
   line numbers or a routine.

   ::

       static timer name="foo_bar" file="foo.c" line=17 to line=18
       dynamic timer routine="int foo1(int)
                     

-  Static and Dynamic phases can be set by specifying either a range of
   line numbers or a routine. If you do not configure TAU with
   ``-PROFILEPHASE`` these phases will be converted to regular timers.

   ::

       static phase routine="int foo(int)
       dynamic phase name="foo1_bar" file="foo.c" line=26 to line=27
                     

-  Loops in the source code can be profiled by specifying a routine in
   which all loop should be profiled, like:

   ::

       loops file="loop_test.cpp" routine="multiply"
                     

-  With `Memory Profiling <#memoryOptions>`__ the following events are
   tracked: memory allocation, memory deallocation, and memory leaks.

   ::

       memory file="foo.f90" routine="INIT"
                     

-  IO Events track the size, in bytes of read, write, and print
   statements.

   ::

       io file="foo.f90" routine="RINB"
                     

Both Memory and IO events are represented along with their call-stack;
the length of which can be set with environment variable
``TAU_CALLPATH_DEPTH``.

    **Note**

    Due to the limitations of the some compilers (IBM xlf, PGI pgf90,
    GNU gfortran), the size of the memory reported for a Fortran Array
    is not the number of bytes but rather the number of elements.

Running an application using DynInstAPI
=======================================

TAU also allows you to dynamically instrument your application using the
DynInst package. There are a few limitation to DyInst: 1) only function
level events will be captured and 2) your application must be compiled
with debugging symbols (``-g``).

To install the DynInstAPI package, configure TAU with -dyinst= option
which will point TAU to where dyninst is installed. Use the ``tau_run``
tool to instrument your application at runtime.

The command-line options accepted by tau\_run are:

::

    Usage: tau_run [-Xrun<Taulibrary> ][-v][-o outfile] \
           [-f <instrumentation file> ] <application> [args]

By default, ``libTAU``. so is loaded by tau\_run. However, the user can
override this and specify another file using the -Xrun<Taulibrary>. In
this case lib<Taulibrary>.so will be loaded using ``LD_LIBRARY_PATH``.

To use ``tau_run``, TAU is configured with DyninstAPI as shown below:

::

    % configure -dyninst=/usr/local/packages/dyninstAPI
    % make install
    % cd tau/examples/dyninst
    % make install
    % tau_run klargest 2500 23
    % pprof; paraprof

Rewriting Binaries
==================

Using MAQAO
-----------

TAU also allows you to rewrite your application using the MAQAO package
included in PDToolkit 3.17 or above(http://tau.uoregon.edu/pdt.tgz).

Install PDToolkit 3.17+ and configure TAU with -pdt= option which will
point TAU to where PDToolkit is installed. Use the ``tau_rewrite`` tool
to instrument your application. (If TAU is not configured with PDT
3.17+, then ``tau_rewrite`` defaults to tau\_run.)

::

    % configure -pdt=/usr/local/packages/pdtoolkit-3.17
    % make install
    % tau_rewrite -T scorep,pdt  -loadlib=/tmp/libfoo.so ./a.out -o a.inst 

Using PEBIL
-----------

TAU also allows you to rewrite your application using the PEBIL package
included in PDToolkit 3.18.1 or above(http://tau.uoregon.edu/pdt.tgz).

Install PDToolkit 3.18.1 and configure TAU with -pdt= option which will
point TAU to where PDToolkit is installed. Use the ``tau_pebil_rewrite``
tool to instrument your application.

::

    % tau_pebil_rewrite -T <commands> -f select.tau <exe> [-o] <output_exe> 

The select.tau file supports outer-loop level instrumentation and
exclude/include lists of functions just like tau\_instrumentor's
select.tau (same format). Also, -T <options> are identical to tau\_exec
-T options.

Using DyninstAPI
----------------

TAU also allows you to rewrite  your application using the DyninstAPI package.

To install the DynInstAPI, configure TAU with -dyninst= options which 
will point TAU to where dyninst is installed, you can also use ``-dyninst=download``, and TAU will automatically
download and install DynInstAPI and its dependencies.

When configuring TAU with DynInstAPI, it will show the environment variables you need to set, which are
``DYNINSTAPI_RT_LIB`` and ``LD_LIBRARY_PATH``

::

    % ./configure -dyninst=download -bfd=download
    % make install
    % tau_run -T <commands> -f select.tau <exe> [-o] <output_exe>;

The select.tau file  supports exclude/include lists of functions just like tau_instrumentor's select.tau (same format).
Also,	-T <options> are identical to tau_exec -T options.
In some cases, flags such as ``-O2`` can prevent DynInstAPI from reading the binaries, if possible,
applications or libraries should be compiled with the flags 
``-g -fno-ipa-sra -fno-ipa-ra -fno-ipa-vrp -fno-omit-frame-pointer`` 

Library Instrumentation with DynInstAPI
----------------
With DynInstAPI instrumentation can be inserted into libraries. The limitations are that the
library should be included in an application using RUNPATH instead of RPATH.

To instrument libraries, tau_run is used with the flag ``-l``. Also, the flag ``-v``
is useful if selective instrumentation is used.
::
    % tau_run -T <commands> -f select.tau -v -l library.so -o INSTRUMENTED_PATH/library.so
    % tau_exec -loadlib=<INSTRUMENTED_PATH/library.so>  [ options ] [--] { exe } [ exe options ]

LD_LIBRARY_PATH can be used instead of ``-loadlib``, but the user must ensure that the correct library is used by the binary.

Profiling each call to a function
=================================

By default TAU profiles the total time (inclusive/exclusive) spent on a
given function. Profiling each function call for an application that
calls some function hundred of thousands of times, is impractical since
the profile data would grow enormously. But configuring TAU with the
``-PROFILEPARAM`` option will have TAU profile select functions each
time they are called. But TAU will also group some of these function
calls together according to the value of the parameter they are given.
For example if a function mpisend(int i) is called 2000 times 1000 times
with 512 and 1000 times with 1024 then we will receive two profile for
mpisend() one we it is called with 512 and one when it is called with
1024. This reduces the overhead since we are profiling mpisend() two
times not 2000 times.

Profiling with Hardware counters
================================

LIST OF COUNTERS:

Set the TAU\_METRICS environment variable with a comma separated list of
metrics or to use the old method set the following values for the
COUNTER<1-25> environment variables.

-  ``GET_TIME_OF_DAY`` - For the default profiling option using
   gettimeofday()

-  ``SGI_TIMERS`` - For ``-SGITIMERS`` configuration option under IRIX

-  ``CRAY_TIMERS`` - For ``-CRAYTIMERS`` configuration option under Cray
   X1.

-  ``LINUX_TIMERS`` - For -LINUXTIMERS configuration option under Linux

-  ``CPU_TIME`` - For user+system time from getrusage() call with
   ``-CPUTIME``

-  ``P_WALL_CLOCK_TIME`` - For PAPI's WALLCLOCK time using
   ``-PAPIWALLCLOCK``

-  ``P_VIRTUAL_TIME`` - For PAPI's process virtual time using
   ``-PAPIVIRTUAL``

-  ``TAU_MUSE`` - For reading counts of Linux OS kernel level events
   when MAGNET/MUSE is installed and -muse configuration option is
   enabled.
   `MUSE <http://public.lanl.gov/radiant/>`__.\ ``TAU_MUSE_PACKAGE``
   environment variable has to be set to package name (busy\_time,
   count, etc.)

-  ``TAU_MPI_MESSAGE_SIZE`` - For tracking the cumulative message size
   for all MPI operations by a node for each routine.

-  ``ENERGY`` - For tracking the power use of the application in joules.
   Requires an -arch=craycnl configuration.

-  ``ACCEL_ENERGY`` - For tracking the power use of the application on
   accelerators in joules. Requires an -arch=craycnl configuration.

    **Note**

    When TAU is configured with -TRACE -MULTIPLECOUNTERS and -papi=<dir>
    options, the COUNTER1 environment variable must be set to
    GET\_TIME\_OF\_DAY to allow TAU's tracing module to use a globally
    synchronized real-time clock for time-stamping event records. When
    we use tracing with hardware performance counters, the counters
    specified in environment variables COUNTER[2-25] are accessed at
    routine transitions and logged in the trace file. Use tau2vtf tool
    to convert TAU traces to VTF3 traces that may be loaded in the
    Vampir trace visualization tool.

and PAPI/PCL options that can be found in ? and ?. Example:

-  ``PCL_FP_INSTR`` - For floating point operations using PCL
   (-pcl=<dir>)

-  ``PAPI_FP_INS`` - For floating point operations using PAPI
   (-papi=<dir>)

-  ``PAPI_NATIVE_<event>`` - For native papi events using PAPI
   (-papi=<dir>)

*NOTE:* When ``-MULTIPLECOUNTERS`` is used with ``-TRACE`` option, the
tracing library uses the wall-clock time from the function specified in
the ``COUNTER1`` variable. This should typically point to wall-clock
time routines (such as ``GET_TIME_OF_DAY or SGI_TIMERS`` or
``LINUX_TIMERS``).

Example:

::

    % setenv COUNTER1   P_WALL_CLOCK_TIME
    % setenv COUNTER2 PAPI_L1_DCM
    % setenv COUNTER3 PAPI_FP_INS

will produce profile files in directories called
``MULT_P_WALL_CLOCK_TIME, MULTI__PAPI_L1_DCM, and MULTI_PAPI_FP_INS.``

+------------------+-------------------------------------------------------+
| TAU\_METRICS     | EVENT Measured                                        |
+==================+=======================================================+
| PAPI\_L1\_DCM    | Level 1 data cache misses                             |
+------------------+-------------------------------------------------------+
| PAPI\_L1\_ICM    | Level 1 instruction cache misses                      |
+------------------+-------------------------------------------------------+
| PAPI\_L2\_DCM    | Level 2 data cache misses                             |
+------------------+-------------------------------------------------------+
| PAPI\_L2\_ICM    | Level 2 instruction cache misses                      |
+------------------+-------------------------------------------------------+
| PAPI\_L3\_DCM    | Level 3 data cache misses                             |
+------------------+-------------------------------------------------------+
| PAPI\_L3\_ICM    | Level 3 instruction cache misses                      |
+------------------+-------------------------------------------------------+
| PAPI\_L1\_TCM    | Level 1 total cache misses                            |
+------------------+-------------------------------------------------------+
| PAPI\_L2\_TCM    | Level 2 total cache misses                            |
+------------------+-------------------------------------------------------+
| PAPI\_L3\_TCM    | Level 3 total cache misses                            |
+------------------+-------------------------------------------------------+
| PAPI\_CA\_SNP    | Snoops                                                |
+------------------+-------------------------------------------------------+
| PAPI\_CA\_SHR    | Request for access to shared cache line (SMP)         |
+------------------+-------------------------------------------------------+
| PAPI\_CA\_CLN    | Request for access to clean cache line (SMP)          |
+------------------+-------------------------------------------------------+
| PAPI\_CA\_INV    | Cache Line Invalidation (SMP)                         |
+------------------+-------------------------------------------------------+
| PAPI\_CA\_ITV    | Cache Line Intervention (SMP)                         |
+------------------+-------------------------------------------------------+
| PAPI\_L3\_LDM    | Level 3 load misses                                   |
+------------------+-------------------------------------------------------+
| PAPI\_L3\_STM    | Level 3 store misses                                  |
+------------------+-------------------------------------------------------+
| PAPI\_BRU\_IDL   | Cycles branch units are idle                          |
+------------------+-------------------------------------------------------+
| PAPI\_FXU\_IDL   | Cycles integer units are idle                         |
+------------------+-------------------------------------------------------+
| PAPI\_FPU\_IDL   | Cycles floating point units are idle                  |
+------------------+-------------------------------------------------------+
| PAPI\_LSU\_IDL   | Cycles load/store units are idle                      |
+------------------+-------------------------------------------------------+
| PAPI\_TLB\_DM    | Data translation lookaside buffer misses              |
+------------------+-------------------------------------------------------+
| PAPI\_TLB\_IM    | Instruction translation lookaside buffer misses       |
+------------------+-------------------------------------------------------+
| PAPI\_TLB\_TL    | Total translation lookaside buffer misses             |
+------------------+-------------------------------------------------------+
| PAPI\_L1\_LDM    | Level 1 load misses                                   |
+------------------+-------------------------------------------------------+
| PAPI\_L1\_STM    | Level 1 store misses                                  |
+------------------+-------------------------------------------------------+
| PAPI\_L2\_LDM    | Level 2 load misses                                   |
+------------------+-------------------------------------------------------+
| PAPI\_L2\_STM    | Level 2 store misses                                  |
+------------------+-------------------------------------------------------+
| PAPI\_BTAC\_M    | BTAC miss                                             |
+------------------+-------------------------------------------------------+
| PAPI\_PRF\_DM    | Prefetch data instruction caused a miss               |
+------------------+-------------------------------------------------------+
| PAPI\_L3\_DCH    | Level 3 Data Cache Hit                                |
+------------------+-------------------------------------------------------+
| PAPI\_TLB\_SD    | Translation lookaside buffer shootdowns (SMP)         |
+------------------+-------------------------------------------------------+
| PAPI\_CSR\_FAL   | Failed store conditional instructions                 |
+------------------+-------------------------------------------------------+
| PAPI\_CSR\_SUC   | Successful store conditional instructions             |
+------------------+-------------------------------------------------------+
| PAPI\_CSR\_TOT   | Total store conditional instructions                  |
+------------------+-------------------------------------------------------+
| PAPI\_MEM\_SCY   | Cycles Stalled Waiting for Memory Access              |
+------------------+-------------------------------------------------------+
| PAPI\_MEM\_RCY   | Cycles Stalled Waiting for Memory Read                |
+------------------+-------------------------------------------------------+
| PAPI\_MEM\_WCY   | Cycles Stalled Waiting for Memory Write               |
+------------------+-------------------------------------------------------+
| PAPI\_STL\_ICY   | Cycles with No Instruction Issue                      |
+------------------+-------------------------------------------------------+
| PAPI\_FUL\_ICY   | Cycles with Maximum Instruction Issue                 |
+------------------+-------------------------------------------------------+
| PAPI\_STL\_CCY   | Cycles with No Instruction Completion                 |
+------------------+-------------------------------------------------------+
| PAPI\_FUL\_CCY   | Cycles with Maximum Instruction Completion            |
+------------------+-------------------------------------------------------+
| PAPI\_HW\_INT    | Hardware interrupts                                   |
+------------------+-------------------------------------------------------+
| PAPI\_BR\_UCN    | Unconditional branch instructions executed            |
+------------------+-------------------------------------------------------+
| PAPI\_BR\_CN     | Conditional branch instructions executed              |
+------------------+-------------------------------------------------------+
| PAPI\_BR\_TKN    | Conditional branch instructions taken                 |
+------------------+-------------------------------------------------------+
| PAPI\_BR\_NTK    | Conditional branch instructions not taken             |
+------------------+-------------------------------------------------------+
| PAPI\_BR\_MSP    | Conditional branch instructions mispredicted          |
+------------------+-------------------------------------------------------+
| PAPI\_BR\_PRC    | Conditional branch instructions correctly predicted   |
+------------------+-------------------------------------------------------+
| PAPI\_FMA\_INS   | FMA instructions completed                            |
+------------------+-------------------------------------------------------+
| PAPI\_TOT\_IIS   | Total instructions issued                             |
+------------------+-------------------------------------------------------+
| PAPI\_TOT\_INS   | Total instructions executed                           |
+------------------+-------------------------------------------------------+
| PAPI\_INT\_INS   | Integer instructions executed                         |
+------------------+-------------------------------------------------------+
| PAPI\_FP\_INS    | Floating point instructions executed                  |
+------------------+-------------------------------------------------------+
| PAPI\_LD\_INS    | Load instructions executed                            |
+------------------+-------------------------------------------------------+
| PAPI\_SR\_INS    | Store instructions executed                           |
+------------------+-------------------------------------------------------+
| PAPI\_BR\_INS    | Total branch instructions executed                    |
+------------------+-------------------------------------------------------+
| PAPI\_VEC\_INS   | Vector/SIMD instructions executed                     |
+------------------+-------------------------------------------------------+
| PAPI\_FLOPS      | Floating Point Instructions executed per second       |
+------------------+-------------------------------------------------------+
| PAPI\_RES\_STL   | Cycles processor is stalled on resource               |
+------------------+-------------------------------------------------------+
| PAPI\_FP\_STAL   | FP units are stalled                                  |
+------------------+-------------------------------------------------------+
| PAPI\_TOT\_CYC   | Total cycles                                          |
+------------------+-------------------------------------------------------+
| PAPI\_IPS        | Instructions executed per second                      |
+------------------+-------------------------------------------------------+
| PAPI\_LST\_INS   | Total load/store instructions executed                |
+------------------+-------------------------------------------------------+
| PAPI\_SYC\_INS   | Synchronization instructions executed                 |
+------------------+-------------------------------------------------------+
| PAPI\_L1\_DCH    | L1 D Cache Hit                                        |
+------------------+-------------------------------------------------------+
| PAPI\_L2\_DCH    | L2 D Cache Hit                                        |
+------------------+-------------------------------------------------------+
| PAPI\_L1\_DCA    | L1 D Cache Access                                     |
+------------------+-------------------------------------------------------+
| PAPI\_L2\_DCA    | L2 D Cache Access                                     |
+------------------+-------------------------------------------------------+
| PAPI\_L3\_DCA    | L3 D Cache Access                                     |
+------------------+-------------------------------------------------------+
| PAPI\_L1\_DCR    | L1 D Cache Read                                       |
+------------------+-------------------------------------------------------+
| PAPI\_L2\_DCR    | L2 D Cache Read                                       |
+------------------+-------------------------------------------------------+
| PAPI\_L3\_DCR    | L3 D Cache Read                                       |
+------------------+-------------------------------------------------------+
| PAPI\_L1\_DCW    | L1 D Cache Write                                      |
+------------------+-------------------------------------------------------+
| PAPI\_L2\_DCW    | L2 D Cache Write                                      |
+------------------+-------------------------------------------------------+
| PAPI\_L3\_DCW    | L3 D Cache Write                                      |
+------------------+-------------------------------------------------------+
| PAPI\_L1\_ICH    | L1 instruction cache hits                             |
+------------------+-------------------------------------------------------+
| PAPI\_L2\_ICH    | L2 instruction cache hits                             |
+------------------+-------------------------------------------------------+
| PAPI\_L3\_ICH    | L3 instruction cache hits                             |
+------------------+-------------------------------------------------------+
| PAPI\_L1\_ICA    | L1 instruction cache accesses                         |
+------------------+-------------------------------------------------------+
| PAPI\_L2\_ICA    | L2 instruction cache accesses                         |
+------------------+-------------------------------------------------------+
| PAPI\_L3\_ICA    | L3 instruction cache accesses                         |
+------------------+-------------------------------------------------------+
| PAPI\_L1\_ICR    | L1 instruction cache reads                            |
+------------------+-------------------------------------------------------+
| PAPI\_L2\_ICR    | L2 instruction cache reads                            |
+------------------+-------------------------------------------------------+
| PAPI\_L3\_ICR    | L3 instruction cache reads                            |
+------------------+-------------------------------------------------------+
| PAPI\_L1\_ICW    | L1 instruction cache writes                           |
+------------------+-------------------------------------------------------+
| PAPI\_L2\_ICW    | L2 instruction cache writes                           |
+------------------+-------------------------------------------------------+
| PAPI\_L3\_ICW    | L3 instruction cache writes                           |
+------------------+-------------------------------------------------------+
| PAPI\_L1\_TCH    | L1 total cache hits                                   |
+------------------+-------------------------------------------------------+
| PAPI\_L2\_TCH    | L2 total cache hits                                   |
+------------------+-------------------------------------------------------+
| PAPI\_L3\_TCH    | L3 total cache hits                                   |
+------------------+-------------------------------------------------------+
| PAPI\_L1\_TCA    | L1 total cache accesses                               |
+------------------+-------------------------------------------------------+
| PAPI\_L2\_TCA    | L2 total cache accesses                               |
+------------------+-------------------------------------------------------+
| PAPI\_L3\_TCA    | L3 total cache accesses                               |
+------------------+-------------------------------------------------------+
| PAPI\_L1\_TCR    | L1 total cache reads                                  |
+------------------+-------------------------------------------------------+
| PAPI\_L2\_TCR    | L2 total cache reads                                  |
+------------------+-------------------------------------------------------+
| PAPI\_L3\_TCR    | L3 total cache reads                                  |
+------------------+-------------------------------------------------------+
| PAPI\_L1\_TCW    | L1 total cache writes                                 |
+------------------+-------------------------------------------------------+
| PAPI\_L2\_TCW    | L2 total cache writes                                 |
+------------------+-------------------------------------------------------+
| PAPI\_L3\_TCW    | L3 total cache writes                                 |
+------------------+-------------------------------------------------------+
| PAPI\_FML\_INS   | FM ins                                                |
+------------------+-------------------------------------------------------+
| PAPI\_FAD\_INS   | FA ins                                                |
+------------------+-------------------------------------------------------+
| PAPI\_FDV\_INS   | FD ins                                                |
+------------------+-------------------------------------------------------+
| PAPI\_FSQ\_INS   | FSq ins                                               |
+------------------+-------------------------------------------------------+
| PAPI\_FNV\_INS   | Finv ins                                              |
+------------------+-------------------------------------------------------+

Table: Events measured by setting the environment variable TAU\_METRICS
in TAU

For example to measure the floating point operations in routines using
``PCL``,

::

    % ./configure -pcl=/usr/local/packages/pcl-1.2
    % setenv PCL_EVENT PCL_FP_INSTR 
    % mpirun -np 8 application

+----------------------------+------------------------------------------------+
| PCL\_EVENT                 | EVENT Measured                                 |
+============================+================================================+
| PCL\_L1CACHE\_READ         | L1 (Level one) cache reads                     |
+----------------------------+------------------------------------------------+
| PCL\_L1CACHE\_WRITE        | L1 cache writes                                |
+----------------------------+------------------------------------------------+
| PCL\_L1CACHE\_READWRITE    | L1 cache reads and writes                      |
+----------------------------+------------------------------------------------+
| PCL\_L1CACHE\_HIT          | L1 cache hits                                  |
+----------------------------+------------------------------------------------+
| PCL\_L1CACHE\_MISS         | L1 cache misses                                |
+----------------------------+------------------------------------------------+
| PCL\_L1DCACHE\_READ        | L1 data cache reads                            |
+----------------------------+------------------------------------------------+
| PCL\_L1DCACHE\_WRITE       | L1 data cache writes                           |
+----------------------------+------------------------------------------------+
| PCL\_L1DCACHE\_READWRITE   | L1 data cache reads and writes                 |
+----------------------------+------------------------------------------------+
| PCL\_L1DCACHE\_HIT         | L1 data cache hits                             |
+----------------------------+------------------------------------------------+
| PCL\_L1DCACHE\_MISS        | L1 data cache misses                           |
+----------------------------+------------------------------------------------+
| PCL\_L1ICACHE\_READ        | L1 instruction cache reads                     |
+----------------------------+------------------------------------------------+
| PCL\_L1ICACHE\_WRITE       | L1 instruction cache writes                    |
+----------------------------+------------------------------------------------+
| PCL\_L1ICACHE\_READWRITE   | L1 instruction cache reads and writes          |
+----------------------------+------------------------------------------------+
| PCL\_L1ICACHE\_HIT         | L1 instruction cache hits                      |
+----------------------------+------------------------------------------------+
| PCL\_L1ICACHE\_MISS        | L1 instruction cache misses                    |
+----------------------------+------------------------------------------------+
| PCL\_L2CACHE\_READ         | L2 (Level two) cache reads                     |
+----------------------------+------------------------------------------------+
| PCL\_L2CACHE\_WRITE        | L2 cache writes                                |
+----------------------------+------------------------------------------------+
| PCL\_L2CACHE\_READWRITE    | L2 cache reads and writes                      |
+----------------------------+------------------------------------------------+
| PCL\_L2CACHE\_HIT          | L2 cache hits                                  |
+----------------------------+------------------------------------------------+
| PCL\_L2CACHE\_MISS         | L2 cache misses                                |
+----------------------------+------------------------------------------------+
| PCL\_L2DCACHE\_READ        | L2 data cache reads                            |
+----------------------------+------------------------------------------------+
| PCL\_L2DCACHE\_WRITE       | L2 data cache writes                           |
+----------------------------+------------------------------------------------+
| PCL\_L2DCACHE\_READWRITE   | L2 data cache reads and writes                 |
+----------------------------+------------------------------------------------+
| PCL\_L2DCACHE\_HIT         | L2 data cache hits                             |
+----------------------------+------------------------------------------------+
| PCL\_L2DCACHE\_MISS        | L2 data cache misses                           |
+----------------------------+------------------------------------------------+
| PCL\_L2ICACHE\_READ        | L2 instruction cache reads                     |
+----------------------------+------------------------------------------------+
| PCL\_L2ICACHE\_WRITE       | L2 instruction cache writes                    |
+----------------------------+------------------------------------------------+
| PCL\_L2ICACHE\_READWRITE   | L2 instruction cache reads and writes          |
+----------------------------+------------------------------------------------+
| PCL\_L2ICACHE\_HIT         | L2 instruction cache hits                      |
+----------------------------+------------------------------------------------+
| PCL\_L2ICACHE\_MISS        | L2 instruction cache misses                    |
+----------------------------+------------------------------------------------+
| PCL\_TLB\_HIT              | TLB (Translation Lookaside Buffer) hits        |
+----------------------------+------------------------------------------------+
| PCL\_TLB\_MISS             | TLB misses                                     |
+----------------------------+------------------------------------------------+
| PCL\_ITLB\_HIT             | Instruction TLB hits                           |
+----------------------------+------------------------------------------------+
| PCL\_ITLB\_MISS            | Instruction TLB misses                         |
+----------------------------+------------------------------------------------+
| PCL\_DTLB\_HIT             | Data TLB hits                                  |
+----------------------------+------------------------------------------------+
| PCL\_DTLB\_MISS            | Data TLB misses                                |
+----------------------------+------------------------------------------------+
| PCL\_CYCLES                | Cycles                                         |
+----------------------------+------------------------------------------------+
| PCL\_ELAPSED\_CYCLES       | Cycles elapsed                                 |
+----------------------------+------------------------------------------------+
| PCL\_INTEGER\_INSTR        | Integer instructions executed                  |
+----------------------------+------------------------------------------------+
| PCL\_FP\_INSTR             | Floating point (FP) instructions executed      |
+----------------------------+------------------------------------------------+
| PCL\_LOAD\_INSTR           | Load instructions executed                     |
+----------------------------+------------------------------------------------+
| PCL\_STORE\_INSTR          | Store instructions executed                    |
+----------------------------+------------------------------------------------+
| PCL\_LOADSTORE\_INSTR      | Loads and stores executed                      |
+----------------------------+------------------------------------------------+
| PCL\_INSTR                 | Instructions executed                          |
+----------------------------+------------------------------------------------+
| PCL\_JUMP\_SUCCESS         | Successful jumps executed                      |
+----------------------------+------------------------------------------------+
| PCL\_JUMP\_UNSUCCESS       | Unsuccessful jumps executed                    |
+----------------------------+------------------------------------------------+
| PCL\_JUMP                  | Jumps executed                                 |
+----------------------------+------------------------------------------------+
| PCL\_ATOMIC\_SUCCESS       | Successful atomic instructions executed        |
+----------------------------+------------------------------------------------+
| PCL\_ATOMIC\_UNSUCCESS     | Unsuccessful atomic instructions executed      |
+----------------------------+------------------------------------------------+
| PCL\_ATOMIC                | Atomic instructions executed                   |
+----------------------------+------------------------------------------------+
| PCL\_STALL\_INTEGER        | Integer stalls                                 |
+----------------------------+------------------------------------------------+
| PCL\_STALL\_FP             | Floating point stalls                          |
+----------------------------+------------------------------------------------+
| PCL\_STALL\_JUMP           | Jump stalls                                    |
+----------------------------+------------------------------------------------+
| PCL\_STALL\_LOAD           | Load stalls                                    |
+----------------------------+------------------------------------------------+
| PCL\_STALL\_STORE          | Store Stalls                                   |
+----------------------------+------------------------------------------------+
| PCL\_STALL                 | Stalls                                         |
+----------------------------+------------------------------------------------+
| PCL\_MFLOPS                | Millions of floating point operations/second   |
+----------------------------+------------------------------------------------+
| PCL\_IPC                   | Instructions executed per cycle                |
+----------------------------+------------------------------------------------+
| PCL\_L1DCACHE\_MISSRATE    | Level 1 data cache miss rate                   |
+----------------------------+------------------------------------------------+
| PCL\_L2DCACHE\_MISSRATE    | Level 2 data cache miss rate                   |
+----------------------------+------------------------------------------------+
| PCL\_MEM\_FP\_RATIO        | Ratio of memory accesses to FP operations      |
+----------------------------+------------------------------------------------+

Table: Events measured by setting the environment variable PCL\_EVENT in
TAU

Using Hardware Performance Counters
===================================

While running the application, set the environment variable
``PCL_EVENT`` or ``TAU_METRICS`` , to specify which hardware performance
counter TAU should use while profiling the application.

    **Note**

    By default, only one counter is tracked at a time. To track more
    than one counter use ``-MULTIPLECOUNTERS``. See ? for more details.

To select floating point instructions for profiling using ``PAPI``, you
would:

::

    % configure -papi=/usr/local/packages/papi-3.5.0
    % make clean install
    % cd examples/papi
    % setenv TAU_METRICS PAPI_FP_INS
    % a.out
        

In addition to the following events, you can use native events (see
``papi_native``) on a given CPU by setting ``TAU_`` to
``PAPI_NATIVE_<event>``. For example:

::

    % setenv PAPI_NATIVE PAPI_NATIVE_PM_BIQ_IDU_FULL_CYC
    % a.out
          

By default ``PAPI`` will profile events in all domains (users space,
kernel, hypervisor, etc). You can restrict the set of domains for papi
event profiling by using the ``TAU_PAPI_DOMAIN`` environment variable
with these values (in a colon separated list, if desired):
``PAPI_DOM_USER,
    PAPI_DOM_KERNEL, PAPI_DOM_SUPERVISOR,`` and ``PAPI_DOM_OTHER`` like
thus:

::

    % setenv TAU_PAPI_DOMAIN PAPI_DOM_SUPERVISOR:PAPI_DOM_OTHER

Profiling with PerfLib
======================

This profiling option is currently under development at LANL.

To configure TAU with PerfLib use the following arguments:

::

    %> configure -perflib=[path_to_perflib lib directory]
                 -perfinc=[path_to_perflib inc directory]
                 -perflibrary=[argument send to the linker if different than default]

After tau is build a new Makefile will be generated with \*-perflib-\*
in its name, use this Makefile when profiling applications with perflib.

After configuration and installation, toggle these three environment
variables before running the application:

::

    %> export PERF_PROFILE=1
    %> export PERF_PROFILE_MPI=1
    %> export PERF_PROFILE_MEMORY=1
    %> export PERF_PROFILE_COUNTERS=1
    %> export PERF_DATA_DIRECTORY=<directory>

We also provide a perf2tau conversion utilities to convert the remaining
perflib profiles to regular tau profiles. To use perf2tau set the
environment variable ``perf_data_directory`` to the type of the
profiling to be converted (the directory where the data is store will be
called something like perf\_data.[type]/). Or you may execute perf2tau
with the type as an argument:

::

    %> perf2tau [type]

See also the man page for perf2tau, ?.

Running a Python application with TAU
=====================================

TAU can automatically instrument all Python routines when the tau python
package is imported. Add <TAUROOT>/<ARCH>/lib/bindings-<options> to the
PYTHONPATH environment variable in order to use the TAU module.

To execute the program, tau.run routine is invoked with the name of the
top level Python code. For e.g.,

::

    #!/usr/bin/env python

    import tau
    from time import sleep

    def f2():
        print "Inside f2: sleeping for 2 secs..."
        sleep(2)
    def f1():
        print "Inside f1, calling f2..."
        f2()

    def OurMain():
        f1()

    tau.run('OurMain()')

instruments routines ``OurMain(), f1() and
    f2()`` although there are no instrumentation calls in the routines.
To use this feature, TAU must be configured with the -pythoninc=<dir>
option (and -pythonlib=<dir> if running under IBM). Before running the
application, the environment variable ``PYTHONPATH`` and
``LD_LIBRARY_PATH`` should be set to include the TAU library directory
(where tau.py is stored). Manual instrumentation of Python sources is
also possible using the Python API and the ``pytau`` package. For e.g.,

::


    #!/usr/bin/env python

    import pytau
    from time import sleep

    x = pytau.profileTimer("A Sleep for excl 5 secs")
    y = pytau.profileTimer("B Sleep for excl 2 secs")
    pytau.start(x)
    print "Sleeping for 5 secs ..."
    sleep(5)
    pytau.start(y)
    print "Sleeping for 2 secs ..."
    sleep(2)
    pytau.stop(y)
    pytau.dbDump()
    pytau.stop(x)

shows how two timers x and y are created and used. Note, multiple timers
can be nested, but not overlapping. Overlapping timers are detected by
TAU at runtime and flagged with a warning (as exclusive time is not
defined when timers overlap).

pprof
=====

pprof sorts and displays profile data generated by TAU. To view the
profile, merely execute pprof in the directory where profile files are
located (or set the ``PROFILEDIR`` environment variable).

::

    % pprof

Its usage is explained below:

::

    usage: pprof [-c|-b|-m|-t|-e|-i] [-r] [-s] [-n num] [-f filename] \
           [-l] [node numbers]
      -c : Sort by number of Calls
      -b : Sort by number of suBroutines called by a function
      -m : Sort by Milliseconds (exclusive time total)
      -t : Sort by Total milliseconds (inclusive time total) (DEFAULT)
      -e : Sort by Exclusive time per call (msec/call)
      -i : Sort by Inclusive time per call (total msec/call)
      -v : Sort by standard deViation (excl usec)
      -r : Reverse sorting order
      -s : print only Summary profile information
      -n num : print only first num functions
      -f filename : specify full path and Filename without node ids 
      -p : suPpress conversion to hh:mm:ss:mmm format
      -l : List all functions and exit 
      -d : Dump output format (for Racy) [node numbers] : prints only info about
        all contexts/threads of given node numbers
     node numbers : prints information about all contexts/threads 
     for specified nodes

Running a JAVA application with TAU
===================================

Java applications are profiled/traced using ``tau_java`` as shown below:

::

    % cd tau/examples/java/pi
    % setenv LD_LIBRARY_PATH $LD_LIBRARY_PATH:<tauroot>/<arch>/lib
    % tau_java  Pi

More information about ``tau_java`` can be found in the Tools section of
the Reference Guide.

Running the application generates profile files with names having the
form profile.<node>.<context>.<thread>. These files can be analyzed
using pprof or paraprof.

Using a tau.conf File
=====================

If a tau.conf file is created, then code that uses that TAU lib will
effected by the settings in tau.conf. For example, if a directory
tau-2.21/tau\_system\_defaults is created and a tau.conf file is placed
in it, TAU will read that file before doing the measurements. A user of
that TAU libs can choose to override the contents of that file by
placing a tau.conf in their own directory. But by default, if the
sysadmin chooses to create this dir, all the users of the TAU libs will
be globally affected by this tau.conf.

For example, tau.conf could be:

::

    % cat tau.conf
    TAU_LOG_PATH=/soft/apps/tau/logs
    PROFILEDIR=$TAU_LOG_DIR
    TAU_PROFILE_FORMAT=merged
    TAU_SUMMARY=1
    TAU_IBM_BG_HWP_COUNTERS=1
    TAU_TRACK_MESSAGE=1
        

Then anyone using TAU from that directory will get
TAU\_IBM\_BG\_HWP\_COUNTERS=1, TAU\_TRACK\_MESSAGE=1, etc.

Using Score-P with TAU
======================

TAU can be configured to use the Score-P measurement infrastructure
(www.score-p.org). To use Score-P, configure TAU with ``-scorep=``
option to point TAU to the Score-P installation. (Please use Score-P
version 1.0 beta or above.) You may then instrument and run your
application with TAU in a manor of your choosing.

Set the environment variable SCOREP\_PROFILING\_FORMAT to TAU\_SNAPSHOT
to produce TAU Snapshot files, which will be found in scorep\*/tau/.
Also, the Score-P library must be found in LD\_LIBRARY\_PATH.

Using UPC with TAU
==================

Please see examples/upc for more details.

To instrument Berkeley UPC with GASP, configure TAU with
``-upcnetwork=<option>`` where option is "mpi" or "udp". Then use a
selective instrumentation file like the one shown below.

::

    BEGIN_INSTRUMENT_SECTION
    forall routine="#"
    loops routine="#"
    barrier routine="#"
    fence routine="#"
    notify routine="#"
    END_INSTRUMENT_SECTION

Then tau\_upc.sh can be used to build the application. If "udp" is used
with -upcnetwork, then upcrun can be used to run the application. For
"mpi", mpirun or a similar mechanism can be used.

To instrument UPC with Cray CCE compilers, the following will produce a
configuration that supports Cray UPC and may be used with tau\_upc.sh

::

    module load PrgEnv-cray
    ./configure -arch=craycnl -pdt=<dir> -pdt_c++=g++

TAU can also build the DMAPP wrapper using Cray CCE compilers. When the
-optDMAPP option is used when building the application with TAU using
TAU\_OPTIONS, DMAPP events are automatically instrumented with
tau\_upc.sh.
