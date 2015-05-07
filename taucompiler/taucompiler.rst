Tau Instrumentation
===================

TAU provides three methods to track the performance of your application.
Library interposition using tau\_exec, compiler directives or source
transformation using PDT. Here is a table that lists the
features/requirement for each method:

+-----------------+------------------------+----------------+--------------------+-----------------------+--------------------------------------------+---------------------------------+------------------------------------------------+--------------------------------------------+
| *Method*        | Requires recompiling   | Requires PDT   | Shows MPI events   | Routine-level event   | Low level events (loops, phases, etc...)   | Throttling to reduce overhead   | Ability to exclude file from instrumentation   | Ability to exclude other regions of code   |
+=================+========================+================+====================+=======================+============================================+=================================+================================================+============================================+
| Interposition   |                        |                | Yes                |                       |                                            | Yes                             |                                                |                                            |
+-----------------+------------------------+----------------+--------------------+-----------------------+--------------------------------------------+---------------------------------+------------------------------------------------+--------------------------------------------+
| Compiler        | Yes                    |                | Yes                | Yes                   |                                            | Yes                             | Yes                                            |                                            |
+-----------------+------------------------+----------------+--------------------+-----------------------+--------------------------------------------+---------------------------------+------------------------------------------------+--------------------------------------------+
| Source          | Yes                    | Yes            | Yes                | Yes                   | Yes                                        | Yes                             | Yes                                            | Yes                                        |
+-----------------+------------------------+----------------+--------------------+-----------------------+--------------------------------------------+---------------------------------+------------------------------------------------+--------------------------------------------+

Table: Different methods of instrumenting applications

The requirements for each method increases as we move down the table:
tau\_exec only requires a system with shared library support. Compiler
based instrumentation requires re-compiling that target application and
Source instrumentation aditionally requires PDT. For this reason we
often recommend that users start with Library interposition and move
down the table if more features are needed.
Dynamic instrumentation through library pre-loading
===================================================

Dynamic instrumentation is achieved through library pre-loading. The
libraries chosen for pre-loading determine the scope of instrumentation.
Some options include tracking MPI, io, memory, cuda, opencl library
calls. MPI instrumentation is included by default the others are enabled
by command-line options to ``tau_exec``. More info at the ```tau_exec``
manual page <#tau_exec>`__. Dynamic instrumentation can be used on both
uninstrumented binaries and binaries instrumented via one of the methods
below, in this way different layers of instrumentation can be combined.

To use ``tau_exec`` place this command before the application executable
when running the application. In this example IO instrumentation is
requested.

::

    %> tau_exec -io ./a.out
    %> mpirun -np 4 tau_exec -io ./a.out

TAU scripted compilation
========================

For more detailed profiles, TAU provides two means to compile your
application with TAU: through your compiler or through source
transformation using PDT.
Compiler Based Instrumentation
------------------------------

TAU provides these scripts: tau\_f90.sh, tau\_cc.sh, and tau\_cxx.sh to
instrument and compile Fortran, C, and C++ programs respectively. You
might use tau\_cc.sh to compile a C program by typing:

::

    %> module load tau
    %> tau_cc.sh -tau_options=-optCompInst samplecprogram.c
        

On machines where a TAU module is not available, you will need to set
the tau makefile and/or options. The makefile and options controls how
will TAU will compile you application. Use

::

    %>tau_cc.sh -tau_makefile=[path to makefile] \
                -tau_options=[option] samplecprogram.c
        

The Makefile can be found in the ``/[arch]/lib`` directory of your TAU
distribution, for example ``/x86_64/lib/Makefile.tau-mpi-pdt``.

You can also use a Makefile specified in an environment variable. To run
tau\_cc.sh so it uses the Makefile specified by environment variable
``TAU_MAKEFILE``, type:

::

    %>export TAU_MAKEFILE=[path to tau]/[arch]/lib/[makefile]
    %>export TAU_OPTIONS=-optCompInst
    %>tau_cc.sh sampleCprogram.c
        

Similarly, if you want to set compile time options like selective
instrumentation you can use the ``TAU_OPTIONS`` environment variable.

Source Based Instrumentation
----------------------------

TAU provides these scripts: tau\_f90.sh, tau\_cc.sh, and tau\_cxx.sh to
instrument and compile Fortran, C, and C++ programs respectively. You
might use tau\_cc.sh to compile a C program by typing:

::

    %> module load tau
    %> tau_cc.sh samplecprogram.c
        

When setting the TAU\_MAKEFILE make sure the Makefile name contains
``pdt`` because you will need a version of TAU built with PDT.

A list of options for the TAU compiler scripts can be found by typing
``man tau_compiler.sh`` or in this chapter of the `reference
guide <#tau_compiler.sh>`__.

Options to TAU compiler scripts
-------------------------------

These are some commonly used options available to the TAU compiler
scripts. Either set them via the ``TAU_OPTIONS`` environment variable or
the ``-tau_options=`` option to ``tau_f90.sh, tau_cc.sh, or tau_cxx.sh``

``-optVerbose``
    Enable verbose output (default: on)
``-optKeepFiles``
    Do not remove intermediate files
``-optShared``
    Use shared library of TAU (consider when using
    tau\_exec

Selectively Profiling an Application
====================================

Custom Profiling
----------------

TAU allows you to customize the instrumentation of a program by using a
selective instrumentation file. This instrumentation file is used to
manually control which parts of the application are profiled and how
they are profiled. If you are using one of the TAU compiler wrapper
scripts to instrument your application you can use the
``-tau_options=-optTauSelectFile=<file>`` option to enable selective
instrumentation.

    **Note**

    Selective instrumentation is only available when using source-level
    instrumentation (PDT).

To specify a selective instrumentation file, create a text file and use
the following guide to fill it in:

-  Wildcards for routine names are specified with the
   #
   mark (because
   \*
   symbols show up in routine signatures.) The
   #
   mark is unfortunately the comment character as well, so to specify a
   leading wildcard, place the entry in quotes.
-  Wildcards for file names are specified with
   \*
   symbols.

::

     
            Here is a example file:
    #Tell tau to not profile these functions
    BEGIN_EXCLUDE_LIST

    void quicksort(int *, int, int)
    # The next line excludes all functions beginning with "sort_" and having 
    # arguments "int *"
    void sort_#(int *)
    void interchange(int *, int *)

    END_EXCLUDE_LIST

    #Exclude these files from profiling
    BEGIN_FILE_EXCLUDE_LIST

    *.so

    END_FILE_EXCLUDE_LIST

    BEGIN_INSTRUMENT_SECTION

    # A dynamic phase will break up the profile into phase where
    # each events is recorded according to what phase of the application
    # in which it occured.
    dynamic phase name="foo1_bar" file="foo.c" line=26 to line=27

    # instrument all the outer loops in this routine
    loops file="loop_test.cpp" routine="multiply"

    # tracks memory allocations/deallocations as well as potential leaks
    memory file="foo.f90" routine="INIT"

    # tracks the size of read, write and print statements in this routine
    io file="foo.f90" routine="RINB"

    END_INSTRUMENT_SECTION

Selective instrumentation files can be created automatically from
``ParaProf`` by right clicking on a trial and selecting the
``Create Selective Instrumentation File`` menu item.
