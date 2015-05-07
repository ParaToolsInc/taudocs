Tracing
=======

How to configure tracing
========================

TAU must be configured with the ``-TRACE`` option to generate event
traces. This can be used in conjunction with ``-PROFILE`` to generate
both profiles and traces. The traces are stored in a directory specified
by the environment variable ``TRACEDIR``, or the current directory, by
default. The environment variables ``TAU_TRACEFILE`` may be used to
specify the name of Vampir trace file. When this variable is set, trace
files are automatically merged and the tau2vtf is invoked to convert the
merged trace file to VTF3 trace format. This conversion takes place on
node 0, thread 0. The intermediate trace files are deleted. To retain
the trace files, the user can set the environment variable
``TAU_KEEP_TRACEFILES`` to true. When ``TAU_TRACEFILE`` is not
specified, the user needs to merge and convert the traces as below.
Example:

::

    % ./configure -arch=sgi64 -TRACE  -mpi -vtf=/usr/local/vtf3-1.34 -slog2
    % make clean; make install
    % setenv TRACEDIR /users/sameer/tracedata/experiment56
    % mpirun -np 4 matrix
        

This generates files named

::

    tautrace.<node>.<context>.<thread>.trc and events.<node>.edf 
        

When generating a Vampir Trace Format (otf or vtf) these environment
variables maybe helpful:

-  ``VT_FILE_PREFIX``\ Prefix used for trace filenames. Default is "a".

-  ``VT_COMPRESSION``\ Write compressed trace files? Default is "yes"

Using the utility tau\_treemerge.pl, these traces are then merged as
shown below:

::

    % tau_treemerge.pl

This generates tau.trc as the merged trace file and tau.edf as the
merged event description file.

tau\_treemerge.pl can take an optional argument (with -n <value>) to
specify the maximum number of trace files to merge in each invocation of
tau\_merge. If we need to merge 2000 trace files and if the maximum
number of open files specified by unix is 250, tau\_treemerge.pl will
incrementally merge the trace files so as not to exceed the number of
open file descriptors. This is important for the IBM BlueGene/L machine
where such restrictions are present on the front-end node.

To convert merged or per-thread traces to another trace format, the
utilities, tau2otf, tau\_convert, tau2vtf, or tau2slog2 are used as
shown below:

::

    Usage: tau2otf [ -n  streams  ] [ -nomessage  ] [ -v  ] [ -z ]
     -n streams : Specifies the number of output streams (default is 1)
     -nomessage : Suppresses printing of message information in the trace
     -v         : Verbose mode sends trace event descriptions to the standard output
     as they are converted
     -z         : Compressed output

Here is an example:

::

    %> tau2otf tau.trc tau.edf out.otf

Converting to Vampir's VTF format:

::

    % tau2vtf
    Usage: tau2vtf <TAU trace> <edf file> <out file> [-a|-fa] 
                   [-nomessage] [-v]
     -a         : ASCII VTF3 file format
     -fa        : FAST ASCII VTF3 file format
     -nomessage : Suppress printing of message information in the trace
     -v         : Verbose
     Default trace format of <out file> is VTF3 binary
     e.g.,
     tau2vtf merged.trc tau.edf app.vpt.gz
    % tau2vtf matrix.trc tau.edf matrix.vpt.gz
    % vampir matrix.vpt.gz
      

To generate slog2 trace files that may be visualized using Jumpshot, we
recommend using the slog2 SDK and Jumpshot bundled with TAU.

::

    % configure -slog2 -TRACE ...
    % tau2slog2 
    tau2slog2 converts a TAU formatted trace file to the SLOG2 format 
              for Jumpshot trace visualizer
    Usage: tau2slog2 <tau_tracefile> <edf_file> -o <slog_tracefile>
    For e.g., 
    % tau2slog2 app.trc tau.edf -o app.slog2
        

To generate traces that may be visualized using Vampir, we recommend
using tau2vtf over the older tau\_convert tool. tau2vtf can produce
binary traces with user-defined events (hardware performance counters
from PAPI etc.) while tau\_convert cannot do this. Binary traces load
faster in Vampir.

::

    % tau_convert
    usage: tau_convert [-alog | -SDDF | -dump | -paraver [-t] | -pv | 
           -vampir [-longsymbolbugfix] [-compact] [-user|-class|-all] 
           [-nocomm]] inputtrc edffile [outputtrc]
     Note: -vampir option assumes multiple threads/node
     Note: -t option used in conjunction with -paraver option assumes 
           multiple threads/node

To view the dump of the trace in text form, use

::

    % tau_convert -dump matrix.trc tau.edf 

tau\_convert can also be used to convert traces to the
`Vampir <http://www.vampir-ng.de/>`__ trace format. For single-threaded
applications (such as the MPI application above), the ``-pv`` option is
used to generate Vampir traces as follows:

::

    % tau_convert -pv matrix.trc tau.edf matrix.pv
    % vampir matrix.vpt.gz &

To convert TAU traces to ``SDDF`` or ``ALOG`` trace formats, ``-SDDF``
and ``-alog`` options may be used. When multiple threads are used on a
node (as with ``-jdk, -pthread or
    -tulipthread`` options during configure), the ``-vampir`` option is
used to convert the traces to the vampir trace format, as shown below:

::


    % tau_convert -vampir smartsapp.trc tau.edf smartsapp.pv
    % vampir smartsapp.pv &

To convert to the Paraver trace format, use the ``-paraver`` option for
single threaded programs and ``-paraver -t`` option for multi-threaded
programs.

*NOTE:* To ensure that inter-process communication events are recorded
in the traces, in addition to the routine transitions, it is necessary
to insert ``TAU_TRACE_SENDMSG`` and ``TAU_TRACE_RECVMSG`` macro calls in
the source code during instrumentation. This is not needed when the TAU
MPI wrapper library is used.

Vampir format traces may be converted to TAU profiles using the
vtf2profile tool.

::

    % vtf2profile -f matrix.vpt.gz -p profiledatadir
    % vtf2profile
    Usage: vtf2profile [options] 
    ***************************HELP***************************
    * '-h' display this help text.                         *
    * '-c' open command line interface.                    *
    * '-f' used as -f <VTF File> where                     *
    *        VTF File is the name of the trace file          *
    *        to be converted to TAU profiles.                *
    * '-p' used as -p <path> where 'path' is the relative  *
    *        path to the directory where profiles are to     *
    *        stored.                                         *
    * '-i' used as -i <from> <to> where 'from' and 'to' are*
    *        integers to mark the desired profiling interval.*
    **********************************************************
