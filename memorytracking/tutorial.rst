TAU Memory Profiling Tutorial
=============================

TAU's memory API options
========================

TAU can evaluate the following memory events:

1. Memory utilization options that examine how much heap memory is
   currently used, and

2. Memory headroom evaluation options that examine how much a program
   can grow (or how much headroom it has) before it runs out of free
   memory on the heap. During memory headroom evaluation TAU tries to
   call malloc with chunks that progressively increase in size, until
   all memory is exhausted. Then it frees those chunks, keeping track of
   how much memory it successfully allocated.

3. Memory leaks in C/C++ programs TAU will track malloc through the
   execuation issuing user event when the program fails to the allocated
   memory.

Using tau\_exec
===============

The ? command allow you to track these memory events with either an
instrumented or uninstrumented binary. If you want to instead track
memory usage in select locations in the source code consider the TAU API
calls below.

Evaluating Memory Utilization
=============================

TAU\_TRACK\_MEMORY
------------------

When ``TAU_TRACK_MEMORY`` is called an interrupt is generated every 10
seconds and the memory event is triggered with the current value. This
interrupt interval can be changed by calling
``TAU_SET_INTERRUPT_INTERVAL(value)``. The tracking of memory events in
both cases can be explictly enabled or disabled by calling the macros
``TAU_ENABLE_TRACKING_MEMORY()`` or ``TAU_DISABLE_TRACKING_MEMORY()``
respectively.

TAU\_TRACK\_MEMORY() can be inserted into the source code:

::

    int main(int argc, char **argv)
    {
        TAU_PROFILE("main()", " ", TAU_DEFAULT);
        TAU_PROFILE_SET_NODE(0);

        TAU_TRACK_MEMORY();

        sleep(12);

        int *x = new int[5*1024*1024];

        sleep(12);

        return 0;
    }

Resulting profile data:

::

    USER EVENTS Profile :NODE 0, CONTEXT 0, THREAD 0
    ---------------------------------------------------------------------------------------
    NumSamples   MaxValue   MinValue  MeanValue  Std. Dev.  Event Name
    ---------------------------------------------------------------------------------------
             2  2.049E+04      2.891  1.024E+04  1.024E+04  Memory Utilization
                (heap, in KB)
    ---------------------------------------------------------------------------------------

TAU\_TRACK\_MEMORY\_HERE
------------------------

Triggers memory tracking at a given execution point. For example:

::

    int main(int argc, char **argv) {
        TAU_PROFILE("main()", " ", TAU_DEFAULT);
        TAU_PROFILE_SET_NODE(0);

        TAU_TRACK_MEMORY_HERE();

        int *x = new int[5*1024*1024];
        TAU_TRACK_MEMORY_HERE();
        return 0;
    }

Here is the resulting profile:

::

    USER EVENTS Profile :NODE 0, CONTEXT 0, THREAD 0
    ---------------------------------------------------------------------------------------
    NumSamples   MaxValue   MinValue  MeanValue  Std. Dev.  Event Name
    ---------------------------------------------------------------------------------------
             2  2.049E+04      2.891  1.024E+04  1.024E+04  Memory Utilization
                (heap, in KB)
    ---------------------------------------------------------------------------------------

TAU\_TRACK\_MEMORY\_FOOTPRINT
-----------------------------

Similar to TAU\_TRACK\_MEMORY but uses the Virtual Memory Resident Set
Size (VmRSS) and High Water Mark (VmHWM) to produce an interval event
and an atomic event respectively.

TAU\_TRACK\_MEMORY\_FOOTPRINT\_HERE
-----------------------------------

Similar to TAU\_TRACK\_MEMORY\_HERE but uses the Virtual Memory Resident
Set Size (VmRSS) and High Water Mark (VmHWM) to produce an interval
event and an atomic event respectively.

-PROFILEMEMORY
--------------

Specifies tracking heap memory utilization for each instrumented
function. When any function entry takes place, a sample of the heap
memory used is taken. This data is stored as user-defined event data in
profiles/traces.

Evaluating Memory Headroom
==========================

TAU\_TRACK\_MEMORY\_HEADROOM()
------------------------------

This call sets up a signal handler that is invoked every 10 seconds by
an interrupt. Inside, it evaluates how much memory it can allocate and
associates it with the callstack. The user can vary the size of the
callstack by setting the environment variable ``TAU_CALLSTACK_DEPTH``
(default is 2). The examples/headroom/track subdirectory has an example
that illustrates the use of this call. To disable tracking this headroom
at runtime, the user may call:
``TAU_DISABLE_TRACKING_MEMORY_HEADROOM()`` and call
``TAU_ENABLE_TRACKING_MEMORY_HEADROOM()`` to re-enable tracking of the
headroom. To set a different interrupt interval, call
``TAU_SET_INTERRUPT_INTERVAL(value)`` where value (in seconds)
represents the inter-interrupt interval.

A sample profile generated has:

::

    USER EVENTS Profile :NODE 0, CONTEXT 0, THREAD 0
    ---------------------------------------------------------------------------------------
    NumSamples   MaxValue   MinValue  MeanValue  Std. Dev.  Event Name
    ---------------------------------------------------------------------------------------
             3       4067       4061       4065      2.828  Memory Headroom Left (in
                MB)
             3       4067       4061       4065      2.828  Memory Headroom
             Left (in MB) : void quicksort(int *, int, int)   => void
             quicksort(int *, int, int)
    --------------------------------------------------------------------------------

TAU\_TRACK\_MEMORY\_HEADROOM\_HERE()
------------------------------------

Sometimes it is useful to track the memory available at a certain point
in the program, rather than rely on an interrupt.
``TAU_TRACK_MEMORY_HEADROOM_HERE()`` allows us to examine the memory
available at a particular location in the source code and associate it
with the currently executing callstack. The examples/headroom/here
subdirectory has an example that illustrates this usage.

::

      ary = new double [1024*1024*50];
        TAU_TRACK_MEMORY_HEADROOM_HERE(); /* takes a sample here!  */
           sleep(1);

A sample profile looks like this:

::

    USER EVENTS Profile :NODE 0, CONTEXT 0, THREAD 0
    ---------------------------------------------------------------------------------------
    NumSamples   MaxValue   MinValue  MeanValue  Std. Dev.  Event Name
    ---------------------------------------------------------------------------------------
             3       3672       3672       3672          0  Memory Headroom Left (in
                MB)
             1       3672       3672       3672          0  Memory Headroom
                            Left (in MB) : main() (calls f1, f5) => f1() (sleeps 1 sec,
                            calls f2, f4)
             1       3672       3672       3672          0  Memory
                            Headroom Left (in MB) : main() (calls f1, f5) => f1()
                            (sleeps 1 sec, calls f2, f4) => f4() (sleeps 4 sec,
                            calls f2)
             1       3672       3672       3672           0  Memory Headroom Left 
                            (in MB) : main() (calls f1, f5) => f5() (sleeps 5 sec)
    ---------------------------------------------------------------------------------------

-PROFILEHEADROOM
----------------

Similar to the -PROFILEMEMORY configuration option that takes a sample
of the memory utilization at each function entry, we now have
``-PROFILEHEADROOM``. In this ``-PROFILEHEADROOM`` option, a sample is
taken at instrumented function's entry and associated with the function
name. This option is meant to be used as a debugging aid due the high
cost associated with executing a series of malloc calls. The cost was
106 microseconds on an IBM BG/L (700 MHz CPU). To use this option,
simply configure TAU with the ``-PROFILEHEADROOM`` option and choose any
method for instrumentation (PDT, MPI, hand instrumentation). You do not
need to annotate the source code in any special way (as is required for
2a and 2b). The examples/headroom/available subdirectory has a simple
example that produces the following profile when TAU is configured with
the ``-PROFILEHEADROOM`` option.

::

    USER EVENTS Profile :NODE 0, CONTEXT 0, THREAD 0
    ---------------------------------------------------------------------------------------
    NumSamples   MaxValue   MinValue  MeanValue  Std. Dev.  Event Name
    ---------------------------------------------------------------------------------------
             1       4071       4071       4071          0  f1() (sleeps 1 sec,
                calls f2, f4) - Memory Headroom Available (MB)
             2       3671       3671       3671          0  f2() (sleeps 2
                sec, calls f3) - Memory Headroom Available (MB)         
             2       3671       3671       3671          0  f3() (sleeps 3 sec) -
                Memory Headroom Available (MB)         
             1       3671       3671       3671          0  f4() (sleeps 4 sec, 
                calls f2) - Memory Headroom Available (MB)         
             1       3671       3671       3671          0  f5() (sleeps 5 sec) - 
                Memory Headroom Available (MB)         
             1       4071       4071       4071          0  main() (calls f1, f5) 
                - Memory Headroom Available (MB)
    ---------------------------------------------------------------------------------------

DetectingMemoryLeaks
====================

TAU's memory leak detection feature can be initiated by giving
tau\_compiler.sh the option ``-optDetectMemoryLeaks``. For a
demonstration consider this C++ program:

::


    #include <stdio.h>
    #include <malloc.h>


    /* there is a memory leak in bar when it is invoked with 5 < value <= 15 */
    int bar(int value)
    {
      printf("Inside bar: %d\n", value);
      int *x;

      if (value > 5)
      {
        printf("looks like it came here from g!\n");
        x = (int *) malloc(sizeof(int) * value);
        x[2]= 2;
        /* do not free it! create a memory leak, unless the value is > 15 */
        if (value > 15) free(x);
      }
      else
      { /* value  <=5 no leak */
        printf("looks like it came here from foo!\n");
        x = (int *) malloc(sizeof(int) * 45);
        x[23]= 2;
        free(x);
      }
      return 0;
    }
        
    int g(int value)
    {
      printf("Inside g: %d\n", value);
      return bar(value);
    }

    int foo(int value)
    {
      printf("Inside f: %d\n", value);
      
      if (value > 5) g(value);
      else bar(value);
        
      return 0;
    }
    int main(int argc, char **argv)
    {
      int *x;
      int *y;
      printf ("Inside main\n");

      foo(12); /* leak */
      foo(20); /* no leak */
      foo(2);  /* no leak */
      foo(13); /* leak */
    }

Notice that bar fails to free allocated memory on input between 5 and 15
and that foo will call g that calls bar when the input to foo is greater
than 5.

Now configuring TAU with ``-PROFILECALLPATH`` run the file by:

::

    %> cd examples/memoryleakdetect/
    %> make
    %> ./simple
    ...
    USER EVENTS Profile :NODE 0, CONTEXT 0, THREAD 0
    ---------------------------------------------------------------------------------------
    NumSamples   MaxValue   MinValue  MeanValue  Std. Dev.  Event Name
    ---------------------------------------------------------------------------------------
             2         52         48         50          2  MEMORY LEAK! malloc size <file=simple.inst.cpp, line=18> : int g(int)   => int bar(int)  
             1         80         80         80          0  free size <file=simple.inst.cpp, line=21>
             1         80         80         80          0  free size <file=simple.inst.cpp, line=21> : int g(int)   => int bar(int)  
             1        180        180        180          0  free size <file=simple.inst.cpp, line=28>
             1        180        180        180          0  free size <file=simple.inst.cpp, line=28> : int foo(int)   => int bar(int)  
             3         80         48         60      14.24  malloc size <file=simple.inst.cpp, line=18>
             3         80         48         60      14.24  malloc size <file=simple.inst.cpp, line=18> : int g(int)   => int bar(int)  
             1        180        180        180          0  malloc size <file=simple.inst.cpp, line=26>
             1        180        180        180          0  malloc size <file=simple.inst.cpp, line=26> : int foo(int)   => int bar(int)  
    ---------------------------------------------------------------------------------------

Notice that the first row show the two Memory leaks along with the
callpath tracing where the unallocated memory was requested.

Memory Tracking In Fortran
==========================

To profile memory usage in Fortran 90 use TAU's ability to selectively
instrument a program. The option ``-optTauSelectFile=<file>`` for
tau\_compilier.sh let you specify a selective instrumentation file which
defines regions of the source code to instrument.

To begin memory profiling, state which file/routines to profile by
typing:

::


    BEGIN_INSTRUMENT_SECTION
    memory file="memory.f90" routine="INIT"
    END_INSTRUMENT_SECTION

Wildcard can be used to instrument multiple routines. For file names \*
character can be used to specify any number of character, thus foo\*
matches foobar, foo2, etc. also for file names ? can match a single
charater, ie. foo? matches foo2, fooZ, but not foobar. You can use # as
a wildcard for routines, ie. b# matches bar, b2z etc.

Memory Profile in Fortran gives you these three metrics:

-  Total size of memory for each ``malloc`` and ``free`` in the source
   code.

-  The callpath for each occurrence of ``malloc`` or ``free``.

-  A list of all variable that were not deallocated in the source code.

    **Note**

    Due to the limitations of the ``xlf`` compiler, The size of the
    memory reported for Fortran Array (compilied with ``xlf``) is not
    the number of bytes but the number of elements.

Here is the profile for the ``example/memoryleakdetect/f90/foo.f90``
file.

::

    %> pprof
    ..
    ---------------------------------------------------------------------------------------
    NumSamples   MaxValue   MinValue  MeanValue  Std. Dev.  Event Name
    ---------------------------------------------------------------------------------------
             1         16         16         16          0  MEMORY LEAK! malloc size <file=foo.f90, var=X, line=7> : MAIN => FOO => BAR 
             2         52         48         50          2  MEMORY LEAK! malloc size <file=foo.f90, var=X, line=7> : MAIN => FOO => G => BAR 
             1         80         80         80          0  free size <file=foo.f90, var=X, line=10>
             1         80         80         80          0  free size <file=foo.f90, var=X, line=10> : MAIN => FOO => G => BAR 
             1        180        180        180          0  free size <file=foo.f90, var=X, line=15>
             1        180        180        180          0  free size <file=foo.f90, var=X, line=15> : MAIN => FOO => BAR 
             1        180        180        180          0  malloc size <file=foo.f90, var=X, line=13>
             1        180        180        180          0  malloc size <file=foo.f90, var=X, line=13> : MAIN => FOO => BAR 
             4         80         16         49      22.69  malloc size <file=foo.f90, var=X, line=7>
             1         16         16         16          0  malloc size <file=foo.f90, var=X, line=7> : MAIN => FOO => BAR 
             3         80         48         60      14.24  malloc size <file=foo.f90, var=X, line=7> : MAIN => FOO => G => BAR 
    ---------------------------------------------------------------------------------------
