Profiling
=========

This chapter describes running an instrumented application, generating
profile data and analyzing that data. Profiling shows the summary
statistics of performance metrics that characterize application
performance behavior. Examples of performance metrics are the CPU time
associated with a routine, the count of the secondary data cache misses
associated with a group of statements, the number of times a routine
executes, etc.

Running the Application
=======================

After instrumentation and compilation are completed, the profiled
application is run to generate the profile data files. These files can
be stored in a directory specified by the environment variable
``PROFILEDIR``. By default, profiles are placed in the current
directory. You can also set the ``TAU_VERBOSE`` enviroment variable to
see the steps the TAU measurement systems takes when your application is
running. Example:

::

    % setenv TAU_VERBOSE 1
    % setenv PROFILEDIR /home/sameer/profiledata/experiment55
    % mpirun -np 4 matrix 

Other environment variables you can set to enable these advanced MPI
measurement features are ``TAU_TRACK_MESSAGE`` to track MPI message
statistics when profiling or messages lines when tracing, and
``TAU_COMM_MATRIX`` to generate MPI communication matrix data.

Reducing Performance Overhead with TAU\_THROTTLE
================================================

TAU automatically throttles short running functions in an effort to
reduce the amount of overhead associated with profiles of such
functions. This feature may be turned off by setting the environment
variable ``TAU_THROTTLE`` to 0. The default rules TAU uses to determine
which functions to throttle is: ``numcalls > 100000 && usecs/call < 10``
which means that if a function executes more than 100000 times and has
an inclusive time per call of less than 10 microseconds, then profiling
of that function will be disabled after that threshold is reached. To
change the values of numcalls and usecs/call the user may optionally set
environment variables:

::

    % setenv TAU_THROTTLE_NUMCALLS 2000000
    % setenv TAU_THROTTLE_PERCALL  5
      

The changes the values to 2 million and 5 microseconds per call.
Functions that are throttled are marked explicitly in there names as
THROTTLED.

Profiling each event callpath
=============================

You can enable callpath profiling by setting the environment variable
``TAU_CALLPATH``. In this mode TAU will recorded the each event callpath
to the depth set by the ``TAU_CALLPATH_DEPTH`` environment variable
(default is two). Because instrumentation overhead will increase with
the depth of the callpath, you should use the shortest call path that is
sufficient.

Using Hardware Counters for Measurement
=======================================

Performance counters exist on many modern microprocessors. They can
count hardware performance events such as cache misses, floating point
operations, etc. while the program executes on the processor. The
Performance Data Standard and ``API (PAPI)`` package provides a uniform
interface to access these performance counters.

To use these counters, you must first find out which PAPI events your
system supports. To do so type:

::

    %> papi_avail 
    Available events and hardware information.
    -------------------------------------------------------------------------
    Vendor string and code   : AuthenticAMD (2)
    Model string and code    : AMD K8 Revision C (15)
    CPU Revision             : 2.000000
    CPU Megahertz            : 2592.695068
    CPU's in this Node       : 4
    Nodes in this System     : 1
    Total CPU's              : 4
    Number Hardware Counters : 4
    Max Multiplex Counters   : 32
    -------------------------------------------------------------------------
    The following correspond to fields in the PAPI_event_info_t structure.

    Name            Code            Avail   Deriv   Description (Note)
    PAPI_L1_DCM     0x80000000      Yes     Yes     Level 1 data cache misses
    PAPI_L1_ICM     0x80000001      Yes     Yes     Level 1 instruction cache misses
    ...

Next, to test the compatibility between each metric you wish papi to
profile, use ``papi_event_chooser:``

::

    papi/utils> papi_event_chooser PAPI_LD_INS PAPI_SR_INS PAPI_L1_DCM
    Test case eventChooser: Available events which can be added with given
    events.
    -------------------------------------------
    Vendor string and code   : GenuineIntel (1)
    Model string and code    : Itanium 2 (2)
    CPU Revision             : 1.000000
    CPU Megahertz            : 1500.000000
    CPU's in this Node       : 16
    Nodes in this System     : 1
    Total CPU's              : 16
    Number Hardware Counters : 4
    Max Multiplex Counters   : 32
    -------------------------------------------
    Event PAPI_L1_DCM can't be counted with others

Here the event chooser tells us that PAPI\_LD\_INS, PAPI\_SR\_INS, and
PAPI\_L1\_DCM are incompatible metrics. Let try again this time removing
PAPI\_L1\_DCM:

::

    % papi/utils> papi_event_chooser PAPI_LD_INS PAPI_SR_INS
    Test case eventChooser: Available events which can be added with given
    events.
    -------------------------------------------
    Vendor string and code   : GenuineIntel (1)
    Model string and code    : Itanium 2 (2)
    CPU Revision             : 1.000000
    CPU Megahertz            : 1500.000000
    CPU's in this Node       : 16
    Nodes in this System     : 1
    Total CPU's              : 16
    Number Hardware Counters : 4
    Max Multiplex Counters   : 32
    -------------------------------------------
    Usage: eventChooser NATIVE|PRESET evt1 evet2 ...

Here the event chooser verifies that PAPI\_LD\_INS and PAPI\_SR\_INS are
compatible metrics.

Next, make sure that you are using a makefile with ``papi`` in its name.
Then set the environment variable ``TAU_METRICS`` to a colon delimited
list of PAPI metrics you would like to use.

::

    setenv TAU_METRICS PAPI_FP_OPS\:PAPI_L1_DCM

In addition to PAPI counters, we support TIME (via unix gettimeofday).
On Linux and CrayCNL systems, we provide the high resolution LINUXTIMERS
metric and on BGL/BGP systems we provide BGLTIMERS and BGPTIMERS.
