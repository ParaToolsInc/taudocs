Tools
=====

tau\_compiler.sh
1
tau\_compiler.sh
Instrumenting source files.
tau\_compiler.sh
-p
profile
-optVerbose
-optQuiet
-optPdtDir=
dir
-optPdtF95Opts=
opts
-optPdtF95Reset=
opts
-optPdtCOpts=
opts
-optPdtCReset=
opts
-optPdtCxxOpts=
opts
-optPdtCReset=
opts
-optPdtF90Parser=
parser
-optGnuFortranParser
-optGnuCleanscapeParser
-optPdtUser=
opts
-optTauInstr=
path
-optDetectMemoryLeaks
-optIncludeMemory
-optTrackUPCR
-optPreProcess
-optCPP=
path
-optCPPOpts=
options
-optCPPReset=
options
-optTauSelectFile=
file
-optPDBFile=
file
-optTau=
opts
-optCompile=
opts
-optTauDefs=
opts
-optTauIncludes=
opts
-optReset=
opts
-optLinking=
opts
-optLinkReset=
opts
-optTauCC=
cc
-optOpariTool=
path/opari
-optOpariDir=
path
-optOpariOpts=
opts
-optOpariReset=
opts
-optOpari2Tool=
path/opari2
-optOpari2ConfigTool=
path/opari2\_config
-optOpari2Dir=
path
-optOpari2Opts=
opts
-optOpari2Reset=
opts
-optNoMpi
-optMpi
-optNoRevert
-optRevert
-optKeepFiles
-optAppC
-optAppCXX
-optAppF90
-optShared
-optCompInst
-optPDTInst
-optDisableHeaderInst
compiler
compiler\_options
-optTauWrapFile=
filename
Description
===========

The TAU Compiler provides a simple way to automatically instrument an
entire project. The TAU Compiler can be used on C, C++, fixed form
Fortran, and free form Fortran.

Options
=======

``-optVerbose`` Turn on verbose debugging messages.

``-optQuiet`` Suppresses excessive output.

``-optDetectMemoryLeaks`` Instructs TAU to detect any memory leaks in
C/C++ programs.TAU then tracks the source location of the memory leak as
wellas the place in the callstack where the memory allocation wasmade.

``-optPdtDir=<dir>`` The PDT architecture directory. Typically
``$(PDTDIR)/$(PDTARCHDIR)``.

``-optPdtF95Opts=<opts>`` Options for Fortran parser in PDT (f95parse).

``-optPdtF95Reset=<opts>`` Reset options to the Fortran parser to the
given list.

``-optPdtCOpts=<opts>`` Options for C parser in PDT (cparse). Typically
``$(TAU_MPI_INCLUDE) $(TAU_INCLUDE) $(TAU_DEFS)``.

``-optPdtCReset=<opts>`` Reset options to the C parser to the given list

``-optPdtCxxOpts=<opts>`` Options for C++ parser in PDT (cxxparse).
Typically ``$(TAU_MPI_INCLUDE) $(TAU_INCLUDE) $(TAU_DEFS)``.

``-optPdtCxxReset=<opts>`` Reset options to the C++ parser to the given
list

``-optPdtF90Parser=<parser>`` Specify a different Fortran parser. For
e.g., ``f90parse`` instead of ``f95parse``.

``-optGnuFortranParser=<parser>`` Specify the GNU ``gfortran`` Fortran
parser ``gfparse``\ instead of ``f95parse``

``-optGnuCleanscapeParser`` Uses the Cleanscape Fortran parser
``f95parse``\ instead of GNU's ``gfparse``

``-optPdtUser=<opts>`` Optional arguments for parsing source code.

``-optTauInstr=<path>`` Specify location of tau\_instrumentor. Typically
``$(TAUROOT)/$(CONFIG_ARCH)/bin/tau_instrumentor``.

``-optIncludeMemory`` Forinteral use only

``-optTrackUPCR`` Adds tracking of the UPC runtime library.

``-optPreProcess`` Preprocess the source code before parsing. Uses
/usr/bin/cpp-P by default.

``-optCPP=<path>`` Specify an alternative preprocessor and pre-process
the sources.

``-optCPPOpts=<options>`` Specify additional options to the C
pre-processor.

``-optCPPReset=<options>`` ResetC preprocessor options to the specified
list.

``-optTauSelectFile=<file>`` Specify selective instrumentation file for
tau\_instrumentor

``-optPDBFile=<file>`` Specify PDB file for tau\_instrumentor. Skips
parsing stage.

``-optTau=<opts>`` Specify options for tau\_instrumentor.

``-optCompile=<opts>`` Options passed to the compiler. Typically ``
               $(TAU_MPI_INCLUDE) $(TAU_INCLUDE) $(TAU_DEFS)
           ``.

``-optTauDefs=<opts>`` Options passed to the compiler by TAU. Typically
``
            $(TAU_DEFS)
    ``.

``-optTauIncludes=<opts>`` Options passed to the compiler by TAU.
Typically ``
    $(TAU_MPI_INCLUDE) $(TAU_INCLUDE)
    ``.

``-optReset=<opts>`` Reset options to the compiler to the given list

``-optLinking=<opts>`` Options passed to the linker. Typically
``$(TAU_MPI_FLIBS) $(TAU_LIBS) $(TAU_CXXLIBS)
           ``.

``-optLinkReset=<opts>`` Reset options to the linker to the given list.

``-optTauCC=<cc>`` Specifies the C compiler used by TAU.

``-optOpariTool=<path/opari>`` Specifies the location of the Opari tool.

``-optOpariDir=<path>`` Specifies the location of the Opari directory.

``-optOpariOpts=<opts>`` Specifies optional arguments to the Opari tool.

``-optOpariReset=<opts>`` Resets options passed to the Opari tool.

``-optNoMpi`` Removes ``-l*mpi*`` libraries during linking (default).

``-optMpi`` Does not remove ``-l*mpi*`` libraries during linking.

``-optNoRevert`` Exit on error. Does not revert to the original
compilation rule on error.

``-optRevert`` Revert to the original compilation rule on error
(default).

``-optKeepFiles`` Does not remove intermediate ``.pdb`` and ``.inst.*``
files.

``-optAppCC`` Sets the failsafe C compiler.

``-optAppCXX`` Sets the failsafe C++ compiler.

``-optAppF90`` Sets the failsafe F90 compiler

``-optShared`` Use shared library version of TAU

``-optCompInst`` Use compiler-based instrumentation

``-optNoCompInst`` Do not revert to compiler instrumentation if source
instrumentation fails.

``-optPDTInst`` Use PDT-based instrumentation

``-optHeaderInst`` Enable instrumentation of headers

``-optDisableHeaderInst`` Disable instrumentation of headers

``-optTrackIO`` Specify wrapping of POSIX I/O calls at link time.

``-optWrappersDir=""`` Specify the location of the link wrappers
directory.

``-optTauUseCXXForC`` Specifies the use of a C++ compiler for compiling
C code

``-optTauWrapFile=<filename>`` Specify path to the link\_options.tau
file generated by tau\_wrap

``-optFixHashIf``

vtf2profile
1
vtf2profile
Generate a TAU profile set from a vampir trace file
vtf2profile
-p
profile
-i
interval\_start
interval\_end
-c
-h
-f
tracefile
Description
===========

vtf2profile is created when TAU is configured with the -vtf=<vtf\_dir>
option. This tool converts a VTF trace file (\*.vpt) to a tau profile
set (profile.A.B.C where A, B and C are the node, context and thread
numbers respectively).

The vtf file to be read is specified in the command line by the -f flag
followed by the file's location. The VTF tracefile specified may be in
gzipped form, eg app.vpt.gz. -p is similarly used to specify the
relative path to the directory where the profile files should be stored.
If no output directory is specified the current directory will be used.
A contiguous interval within the vtf file may be selected for conversion
by using the -i flag followed by two integers, representing the
timestamp of the start and end of the desired interval respectively. The
entire vtf file is converted if no interval is given.

Options
=======

``-f tracefile`` -Specify the Vampir tracefile to be converted.

``-p profile`` -Specify the location where the profile file(s) should be
written.

``-i interval_start interval_end`` -Limit the profile produced to the
specified interval within the vampir trace file.

``-c`` -Opens a command line interface for the program.

``-h`` -Displays a help message.

Examples
========

To convert a vampir tracefile, trace.vpt, to an equivalent TAU profile,
use the following:

::

    vtf2profile -f trace.vpt
        

To produce a TAU profile in the ./profiles directory representing only
the events from the start of the tracefile to timestamp 6000, use:

::

    vtf2profile -f trace.vpt -p ./profiles -i 0 6000
        

See Also
========

?, ?

tau2vtf
1
tau2vtf
convert TAU tracefiles to vampir tracefiles
tau2vtf
-nomessage
-v
-a
-fa
tau\_tracefile
tau\_eventfile
vtf\_tracefile
Description
===========

This program is generated when TAU is configured with the
-vtf=<vtf\_dir> option.

The tau2vtf trace converter takes a single tau\_tracefile (\*.trc) and
tau\_eventfile (\*.edf) and produces a corresponding vtf\_tracefile
(\*.vtf). The input files and output file must be specified in that
order. Multi-file TAU traces must be merged before conversion.

The default output file format is VTF3 binary. If the output filename is
given as the .vpt.gz type, rather than .vpt, the output file will be
gzipped. There are two additional output format options. The command
line argument '-a' produces the vtf file output in ASCII VTF3 format.
The command line argument '-fa' produces the vtf file output in the FAST
ASCII VTF3 format. Note that these arguments are mutually exclusive.

Options
=======

``-nomessage`` Suppresses printing of message information in the trace.

``-v`` Verbose mode sends trace event descriptions to the standard
output as they are converted.

``-a`` Print the vtf file output in the human-readable VTF3 ASCII format

``-fa`` Print the vtf file in the simplified human-readable FAST ASCII
VTF3 format

Examples
========

The program must be run with the tau trace, tau event and vtf output
files specified in the command line in that order. Any additional
arguments follow. The following will produce a VTF, app.vpt, from the
TAU trace and event files merged.trc and tau.edf trace file:

::

    tau2vtf merged.trc tau.edf app.vpt
          

The following will convert merged.trc and tau.edf to a gzipped FAST
ASCII vampir tracefile app.vpt.gz, with message events omitted:

::

    tau2vtf merged.trc tau.edf app.vpt.gz -nomessage -fa
          

See Also
========

?, ?, ?, ?

trace2profile
1
trace2profile
convert TAU tracefiles to TAU profile files
tau2vprofile
-d
directory
-s
snapshot\_interval
tau\_tracefile
tau\_eventfile
Description
===========

This program is generated when TAU is configured with the -TRACE option.

The trace2profile converter takes a single tau\_tracefile (\*.trc) and
tau\_eventfile (\*.edf) and produces a corresponding series of profile
files. The input files must be specified in that order, with optinal
parameters coming afterward. Multi-file TAU traces must be merged before
conversion.

Options
=======

``-d`` Output profile files to the specified 'directory' rather than the
current directory.

``-s`` Output a profile snapshot showing the state of the profile data
accumulated from the trace every 'snapshot\_interval' time units. The
snapshot profiles are placed sequentially in directories labled
'snapshot\_n' where 'n' is an integer ranging from 0 to to the total
number of snapshots -1.

Examples
========

The program must be run with the tau trace and tau event files specified
in the command line in that order. Any additional arguments follow. The
following will produce a profile file array, from the TAU trace and
event files merged.trc and tau.edf trace file:

::

    trace2profile merged.trc tau.edf
          

The following will convert merged.trc and tau.edf to a series of
profiles one directory higher. It will also produce a profile snapshot
every 250,000 time units:

::

    trace2profile merged.trc tau.edf -d ./.. -s 250000
          

See Also
========

?, ?, ?, ?, ?

tau2elg
1
tau2elg
convert TAU tracefiles to Epilog tracefiles
tau2elg
-nomessage
-v
tau\_tracefile
tau\_eventfile
elg\_tracefile
Description
===========

This program is generated when TAU is configured with the
-epilog=<epilog\_dir> option.

The tau2elg trace converter takes a tau trace file (\*.trc) and event
definition file (\*.edf) and produces a corresponding epilog binary
trace file (\*.elg). Multi-file TAU traces must be merged before
conversion.

Options
=======

``-nomessage`` Suppresses printing of message information in the trace.

``-v`` Verbose mode sends trace event descriptions to the standard
output as they are converted.

Examples
========

The program must be run with the tau trace, tau event and elg output
files specified in the command line in that order. Any additional
arguments follow. The following would convert merged.trc and tau.edf to
the Epilog tracefile app.elg, with message events omitted:

::

    ./tau2vtf merged.trc tau.edf app.elg -nomessage
          

See Also
========

?

tau2slog2
1
tau2slog2
convert TAU tracefiles to SLOG2 tracefiles
tau2slog2
options
tau\_tracefile
tau\_eventfile
-o
output.slog2
Description
===========

This program is generated when TAU is configured with the -slog2 or
-slog2=<slog2\_dir> option.

The tau2slog2 trace converter takes a single tau trace file (\*.trc) and
event definition file (\*.edf) and produces a corresponding slog2 binary
trace file (\*.slog2).

The tau2slog2 converter is called from the command line with the
locations of the tau trace and event files. These arguments must be
followed by the -o flag and the name of the slog2 file to be written.
tau2slog 2 accepts no other arguments.

Options
=======

``[-h|--h|-help|--help]`` Display HELP message.

`` [-tc]`` Check increasing endtime order, exit when 1st violation
occurs.

`` [-tcc]`` Check increasing endtime order,continue when violations
occur.

`` [-nc number]`` Number of childern per node (default is 2)

`` [-ls number]`` Max byte size of leaf nodes (default is 65536)

`` [-o output.slog2]`` Output filename with slog2 suffix

Examples
========

A typical invocation of the converter, to create app.slog2, is as
follows:

::

    tau2slog2 app.trc tau.edf -o app.slog2
          

See Also
========

?, ?

tau2otf
1
tau2otf
convert TAU tracefiles to OTF tracefiles for Vampir/VNG
tau2otf
-n
streams
-nomessage
-v
Description
===========

This program is generated when TAU is configured with the
-otf=<otf\_dir> option. The tau2otf trace converter takes a TAU
formatted tracefile (\*.trc) and a TAU event description file (\*.edf)
and produces an output trace file in the Open Trace Format (OTF). The
user may specify the number of output streams for OTF. The input files
and output file must be specified in that order. TAU traces should be
merged using tau\_merge prior to conversion.

Options
=======

``-n`` streams Specifies the number of output streams (default is 1).
``-nomessage`` Suppresses printing of message information in the trace.
``-v`` Verbose mode sends trace event descriptions to the standard
output as they are converted.

Examples
========

The program must be run with the tau trace, tau event and otf output
files specified in the command line in that order. Any additional
arguments follow. The following will produced an OTF file, a pp.otf and
other related event and definition files, from the TAU trace and event
files merged.trc and tau.edf trace file:

::

    tau2otf merged.trc tau.edf app.otf

See Also
========

tau2vtf(1), trace2profile(1), vtf2profile(1), tau\_merge(1),
tau\_convert(1)

tau2otf2
1
tau2otf2
convert TAU tracefiles to OTF2 tracefiles for Vampir/VNG
tau2otf2
-n
streams
-nomessage
-v
Description
===========

This program is generated when TAU is configured with the
-otf=<otf\_dir> option. The tau2otf2 trace converter takes a TAU
formatted tracefile (\*.trc) and a TAU event description file (\*.edf)
and produces an output trace file in the Open Trace Format (OTF2). The
user may specify the number of output streams for OTF2. The input files
and output file must be specified in that order. TAU traces should be
merged using tau\_merge prior to conversion.

Options
=======

``-n`` streams Specifies the number of output streams (default is 1).
``-nomessage`` Suppresses printing of message information in the trace.
``-v`` Verbose mode sends trace event descriptions to the standard
output as they are converted.

Examples
========

The program must be run with the tau trace, tau event and otf2 output
files specified in the command line in that order. Any additional
arguments follow. The following will produced an OTF2 file, a pp.otf2
and other related event and definition files, from the TAU trace and
event files merged.trc and tau.edf trace file:

::

    tau2otf2 merged.trc tau.edf app.otf2

See Also
========

tau2vtf(1), trace2profile(1), vtf2profile(1), tau\_merge(1),
tau\_convert(1)

perf2tau
1
perf2tau
converts PerfLib profiles to TAU profile files
perf2tau
data\_directory
-h
-flat
Description
===========

Converts perflib data to TAU format.

If an argument is not specified, it checks the perf\_data\_directory
environment variable. Then opens perf\_data.timing directory to read
perflib data If no args are specified, it tries to read
perf\_data.<current\_date> file.

Options
=======

``-h`` Display the help information.

``-flat`` Suppresses callpath profiles, each callpath profile will be
flattened to show only the function profile.

Examples
========

::

    %> perf2tau timing
          

See Also
========

?, ?, ?, ?, ?

tau\_merge
1
tau\_merge
combine multiple node and or thread TAU tracefiles into a merged
tracefile
tau\_merge
-a
-r
-n
-e
eventfile\_list
-m
output\_eventfile
tracefile\_list
output\_tracefile
-
Description
===========

tau\_merge is generated when TAU is configured with the -TRACE option.

This tool assembles a set of tau trace and event files from multiple
multiple nodes or threads across a program's execution into a single
unified trace file. Many TAU trace file tools operate on merged trace
files.

Minimally, tau\_merge must be invoked with a list of unmerged trace
files followed by the desired name of the merged trace file or the -
flag to send the output to the standard out. Typically the list can be
designated by giving the shared name of the trace files to be merged
followed by desired range of thread or node designators in brackets or
the wild card character '\*' to encompass variable thread and node
designations in the filename (trace.A.B.C.trc where A, B and C are the
node, context and thread numbers respectively). For example
tautrace.\*.trc would represent all tracefiles in a given directory
while tautrace.[0-5].0.0.trc would represent the tracefiles of nodes 0
through 5 with context 0 and thread 0.

tau\_merge will generate the specified merged trace file and an event
definition file, tau.edf by default.

The event definition file can be given an alternative name by using the
'-m' flag followed by the desired filename. A list of event definition
files to be merged can be designated explicitly by using the '-e' flag
followed by a list of unmerged .edf files, specified in the same manner
as the trace file list.

If computational resources are insufficient to merge all trace and event
files simultaneously the process may be undertaken hierarchically.
Corresponding subsets of the tracefiles and eventfiles may be merged in
sequence to produce a smaller set of files that can then be to merged
into a singular fully merged tracefile and eventfile. E.g. for a 100
node trace, trace sets 1-10, 11-20, ..., 91-100 could be merged into
traces 1a, 2a, ..., 10a. Then 1a-10a could be merged to create a fully
merged tracefile.

Options
=======

``-e`` eventfile\_list explicitly define the eventfiles to be merged

``-m`` output\_eventfile explicitly name the merged eventfile to be
created

``-`` send the merged tracefile to the standard out

``-a`` adjust earliest timestamp time to zero

``-r`` do not reassemble long events

``-n`` do not block waiting for new events. By default tau\_merge will
block and wait for new events to be appended if a tracefile is
incomplete. This command allows offline merging of (potentially)
incomplete tracefiles.

Examples
========

To merge all TAU tracefiles into app.trc and produce a merged tau.edf
eventfile:

::

    tau_merge *.trc app.trc
          

To merge all eventfiles 0-255 into ev0\_255merged.edf and TAU tracefiles
for nodes 0-255 into the standard out:

::

    tau_merge -e events.[0-255].edf -m ev0_255merged.edf \
      tautrace.[0-255].*.trc -
          

To merge eventfiles 0, 5 and seven info ev057.edf and tau tracefiles for
nodes 0, 5 and 7 with context and thread 0 into app.trc:

::

    tau_merge -e events.0.edf events.5.edf events.7.edf -m ev057.edf \
      tautrace.0.0.0.trc tautrace.5.0.0.trc tautrace.7.0.0.trc app.trc
          

See Also
========

`tau\_convert <#tau_convert>`__

`trace2profile <#trace2profile>`__

`tau2vtf <#tau2vtf>`__

`tau2elg <#tau2elg>`__

`tau2slog2 <#tau2slog2>`__

tau\_treemerge.pl
1
tau\_treemerge.pl
combine multiple node and or thread TAU tracefiles into a merged
tracefile
tau\_treemerge.pl
-n
break\_amount
Description
===========

tau\_treemerge.pl is generated when TAU is configured with the -TRACE
option.

This tool assembles a set of tau trace and event files from multiple
multiple nodes or threads across a program's execution into a single
unified trace file. Many TAU trace file tools operate on merged trace
files.

tau\_treemerge.pl will generate the specified merged trace file and an
event definition file, tau.edf by default.

Options
=======

``-n`` break\_amount set the maximum number of trace files to merge in
each invocation of tau\_merge. If we need to merge 2000 trace files and
if the maximum number of open files specified by unix is 250,
tau\_treemerge.pl will incrementally merge the trace files so as not to
exceed the number of open file descriptors.

See Also
========

`tau\_merge <#tau_merge>`__

`tau\_convert <#tau_convert>`__

`trace2profile <#trace2profile>`__

`tau2vtf <#tau2vtf>`__

`tau2elg <#tau2elg>`__

`tau2slog2 <#tau2slog2>`__

tau\_convert
1
tau\_convert
convert TAU tracefiles into various alternative trace formats
tau\_convert
-alog
-SSDF
-dump
-paraver
-t
-pv
-vampir
-longsymbolbugfix
-compact
-user
-class
-all
-nocomm
outputtrc
inputtrc
edffile
Description
===========

tau\_convert is generated when TAU is configured with the -TRACE option.

This program requires specification of a TAU tracefile and eventfile. It
will convert the given TAU traces to the ASCII-based trace format
specified in the first argument. The conversion type specification may
be followed by additional options specific to the conversion type. It
defaults to the single threaded vampir format if no other format is
specified. tau\_convert also accepts specification of an output file as
the last argument. If none is given it prints the converted data to the
standard out.

Options
=======

``-alog`` convert TAU tracefile into the alog format (This format is
deprecated. The SLOG2 format is recommended.)

``-SDDF`` convert TAU tracefile into the SDDF format

``-dump`` convert TAU tracefile into multi-column human readable text

``-paraver`` convert TAU tracefile into paraver format

``-t`` indicate conversion of multi threaded TAU trace into paraver
format

``-pv`` convert single threaded TAU tracefile into vampir format (all
-vampir options apply) (default)

``-vampir`` convert multi threaded TAU tracefile into vampir format

``-longsymbolbugfix`` make the first characters of long, similar
identifier strings unique to avoid a bug in vampir

``-compact`` abbreviate individual event entries

``-all`` compact all entries (default)

``-user`` compact user entries only

``-class`` compact class entries only

``-nocomm`` disregard communication events

``[outputtrc]`` specify the name of the output tracefile to be produced

Examples
========

To print the contents of a TAU tracefile to the screen:

::

    tau_convert -dump app.trc tau.edf
          

To convert a merged, threaded TAU tracefile to paraver format:

::

      
    tau_convert -paraver -t app.trc tau.edf app.pv 
          

See Also
========

?, ?, ?, ?

tau\_reduce
1
tau\_reduce
generates selective instrumentation rules based on profile data
tau\_reduce
-f
filename
-n
-r
filename
-o
filename
-v
-p
Description
===========

tau\_reduce is an application that will apply a set of user-defined
rules to a pprof dump file (``pprof -d``) in order to create a select
file that will include an exclude list for selective implementation for
TAU. The user must specify the name of the pprof dump file that this
application will use. This is done with the -f filename flag. If no rule
file is specified, then a single default rule will be applied to the
file. This rule is: numcalls > 1000000 & usecs/call < 2, which will
exclude all routines that are called at least 1,000,000 times and
average less then two microseconds per call. If a rule file is
specified, then this rule is not applied. If no output file is
specified, then the results will be printed out to the screen.

Rules
=====

Users can specify a set of rules for tau\_reduce to apply. The rules
should be specified in a separate file, one rule per line, and the file
name should be specifed with the appropriate option on the command line.
The grammar for a rule is: [GROUPNAME:]FIELD OPERATOR NUMBER. The
GROUPNAME followed by the colon (:) is optional. If included, the rule
will only be applied to routines that are a member of the group
specified. Only one group name can be applied to each rule, and a rule
must follow a groupname. If only a groupname is given, then an
unrecognized field error will be returned. If the desired effect is to
exclude all routines that belong to a certain group, then a trivial
rule, such as GROUP:numcalls > -1 may be applied. If a groupnameis
given, but the data does not contain any groupname data, then then an
error message will be given, but the rule will still be applied to the
date ignoring the groupname specification. A FIELD is any of the routine
attributes listed in the following table:

::

    ATTRIBUTE NAME     MEANING  
    numcalls           Number of times the routine is called    
    numsubrs           Number of subroutines that the routine contains  
    percent            Percent of total implementation time 
    usec               Exclusive routine running time, in microseconds  
    cumusec            Inclusive routine running time, in microseconds  
    count              Exclusive hardware count 
    totalcount         Inclusive hardware count 
    stddev             Standard deviation   
    usecs/call         Microseconds per call    
    counts/call        Hardware counts per call
        

+------------------+---------------------------------------------------+
| ATTRIBUTE NAME   | MEANING                                           |
+==================+===================================================+
| numcalls         | Number of times the routine is called             |
+------------------+---------------------------------------------------+
| numsubrs         | Number of subroutines that the routine contains   |
+------------------+---------------------------------------------------+
| percent          | Percent of total implementation time              |
+------------------+---------------------------------------------------+
| usec             | Exclusive routine running time, in microseconds   |
+------------------+---------------------------------------------------+
| cumusec          | Inclusive routine running time, in microseconds   |
+------------------+---------------------------------------------------+
| count            | Exclusive hardware count                          |
+------------------+---------------------------------------------------+
| totalcount       | Inclusive hardware count                          |
+------------------+---------------------------------------------------+
| stddev           | Standard deviation                                |
+------------------+---------------------------------------------------+
| usecs/call       | Microseconds per call                             |
+------------------+---------------------------------------------------+
| counts/call      | Hardware counts per call                          |
+------------------+---------------------------------------------------+

Table: Selection Attributes

Some FIELDS are only available for certain files. If hardware counters
are used, then usec, cumusec, usecs/per call are not applicable and a
error is reported. The opposite is true if timing data is used rather
than hardware counters. Also, stddev is only available for certain files
that contain that data.

An OPERATOR is any of the following: < (less than), > (greater than), or
= (equals).

A NUMBER is any number.

A compound rule may be formed by using the & (and) symbol in between two
simple rules. There is no "OR" because there is an implied or between
two separate simple rules, each on a separate line. (ie the compound
rule usec < 1000 OR numcalls = 1 is the same as the two simple rules
"usec < 1000" and "numcalls = 1").

Rule Examples
=============

::

    #exclude all routines that are members of TAU_USER and have less than
    #1000 microseconds
    TAU_USER:usec < 1000

    #exclude all routines that have less than 1000 microseconds and are
    #called only once.
    usec < 1000 & numcalls = 1

    #exclude all routines that have less than 1000 usecs per call OR have a percent
    #less than 5
    usecs/call < 1000
    percent < 5
        

NOTE: Any line in the rule file that begins with a # is a comment line.
For clarity, blank lines may be inserted in between rules and will also
be ignored.

Options
=======

``-f`` filename specify filename of pprof dump file

``-p`` print out all functions with their attributes

``-o`` filename specify filename for select file output (default: print
to screen

``-r`` filename specify filename for rule file

``-v`` verbose mode (for each rule, print out rule and all functions
that it excludes)

Examples
========

To print to the screen the selective instrumentation list for the
paraprof dump file app.prf with default selection rules use:

::

    tau_reduce -f app.prf
          

To create a selection file, app.sel, from the paraprof dump file app.prf
using rules specified in foo.rlf use:

::

    tau_reduce -f app.prf -r foo.rlf -o app.sel
          

See Also
========

tau\_ompcheck
1
tau\_ompcheck
Completes uncompleted do/for/parallel omp directives
tau\_ompcheck
pdbfile
sourcefile
-o
outfile
-v
-d
Description
===========

Finds uncompleted do/for omp directives and inserts closing directives
for each one uncompleted. do/for directives are expected immediately
before a do/for loop. Closing directives are then placed immediately
following the same do/for loop.

Options
=======

``pdbfile`` A pdbfile generated from the source file you wish to check.
This pdbfile must contain comments from which the omp directives are
gathered. See pdbcomment for information on how to obtain comment from a
pdbfile.

``sourcefile`` A fortran, C or C++ source file to analyzed.

``-o`` write the output to the specified outfile.

``-v``\ verbose output, will say which directive where added.

``-d`` debuging information, we suggest you pipe this unrestrained
output to a file.

Examples
========

To check file: source.f90 do: (you will need pdtoolkit/<arch>/bin and
tau/utils/ in your path).

::

    %>f95parse source.f90
    %>pdbcomment source.pdb > source.comment.pdb
    %>tau_omp source.comment.pdb source.f90 -o source.chk.f90
        

See Also
========

f95parse pdbcomment

tau\_poe
1
tau\_poe
Instruments a MPI application while it is being executed with poe.
tau\_poe
-XrunTAUsh-
tauOptions
applcation
poe options
Description
===========

This tool dynamically instruments a mpi application by loading a
specific mpi library file.

Options
=======

``tauOptions`` To instrument a mpi application a specific TAU library
file is loaded when the application is executed. To select which library
is loaded use this option. The library files are build according to the
options set when TAU is configured. The library file that have been
build and thus available for use are in the [TAU\_HOME]/[arch]/lib
directory. The file are listed as libTAUsh-\*.so where \* is the
instrumentation options. For example to use the
libTAUsh-pdt-openmp-opari.so file let the comman line option be
-XrunTAUsh-pdt-openmp-opari.

Examples
========

Instrument a.out wit the currently configured options and then run it on
four nodes:

::

    %>tau_poe ./a.out -procs 4
        

Select the libTAUsh-mpi.so library to instrument a.out with:

::

    %>tau_poe -XrunTAUsh-mpi ./a.out -procs 4
            

tau\_validate
1
tau\_validate
Validates a TAU installation by performing various tests on each TAU
stub Makefile
tau\_validate
-v
--html
--build
--run
--tag
arch directory
Description
===========

tau\_validate will attempt to validate a TAU installation by performing
various tests on each TAU stub Makefile. Some degree of logic exists to
know where a given test applies to a given makefile, but it's not
perfect.

Options
=======

``v`` Verbose output

``html`` Output results in HTML

``build`` Only build

``run`` Only run

``tag`` Only check configurations containing the tag. ie. ``--tag
        papi`` checks only libraries with the ``-papi`` in their name.

``arch directory`` Specify an arch directory (e.g. rs6000), or the lib
directory (rs6000/lib), or a specific makefile. Relative or absolute
paths are ok.

Example
=======

There is a few examples:

::

        
    bash : ./tau_validate --html x86_64 &> results.html
    tcsh : ./tau_validate --html x86_64 >& results.html

tauex
1
tauex
Allows you to choose a tau configuration at runtime
tauex
OPTION
--
executable
executable options
Description
===========

Use this script to dynamically load a TAU profiling/tracing library or
to select which papi events/domain to use during execuation of the
application. At runtime tauex will set the LD\_LIBRARY\_PATH and pass
any other parameters (or papi events) to the program and execute it with
the specified TAU measurement options.

Options
=======

-d
    Enable debugging output, use repeatedly for more output.

-h
    Print help message.

-i
    Print information about the host machine.

-s
    Dump the shell environment variables and exit.

-U
    User mode counts

-K
    Kernel mode counts

-S
    Supervisor mode counts

-I
    Interrupt mode counts

-l
    List events

-L <event>
    Describe event

-a
    Count all native events (implies -m)

-n
    Multiple runs (enough runs of exe to gather all events)

-e <event>
    Specify PAPI preset or native event

-T <option>
    Specify TAU option

-v
    Debug/Verbose mode

-XrunTAU-<options>
    specify TAU library directly

Notes
=====

Defaults if unspecified: -U -T MPI,PROFILE -e P\_WALL\_CLOCK\_TIME MPI
is assumed unless SERIAL is specified PROFILE is assumed unless one of
TRACE, VAMPIRTRACE or EPILOG is specified P\_WALL\_CLOCK\_TIME means
count real time using fastest available timer

Example
=======

``mpirun -np 2 tauex -e PAPI_TOT_CYC -e PAPI_FP_OPS -T MPI,PROFILE --
     ./ring``

tau\_exec
1
tau\_exec
TAU execution wrapping script
tau\_exec
options
--
exe
exe options
Description
===========

Use this script to perform memory or IO tracking on either an
instrumented or uninstrumented executable.

Options
=======

-v
    verbose mode

-qsub
    BG/P qsub mode

-io
    track io

-memory
    track memory

-cuda
    track GPU events via CUDA (Must be configured with -cuda=<dir>,
    Preferred of CUDA 4.0 or earlier)

-cupti
    track GPU events via Nvidia's CUPTI interface (Must be configured
    with -cupti=<dir>, Preferred for CUDA 4.1 or later).

-um
    in conjunction with -cupti adds support for the Unified Memory GPUs.
    Requires CUDA 6.5 or later.

-opencl
    track GPU events via OpenCL

-openacc
    track openacc events. Supports TAU configurations with -arch=craycnl
    or PGI compilers on x86\_64 Linux

-armci
    track ARMCI events via PARMCI (Must be configured with -armci=<dir>)

-ebs
    enable Event-based sampling. See README.sampling for more
    information

-ebs\_period=<count >
    sampling period (default 1000)

-ebs\_source=<counter>
    sets sampling metric (default "itimer")

-T<option>
    : specify TAU option

-loadlib=<file.so >
    : specify additional load library

-XrunTAU-<options>
    specify TAU library directly

Notes
=====

Defaults if unspecified: -T MPI. MPI is assumed unless SERIAL is
specified

CUDA kernel tracking is included, if A CUDA SYNC call is made after each
kernel launch and ``cudaThreadExit()`` is called before the exit of each
thread that uses CUDA.

OPENCL kernel tracking is included, if A OPENCL SYNC call is made after
each kernel launch and ``clReleaseContext()`` is called before the exit
of each thread that uses CUDA.

Examples
========

``mpirun -np 2 tau_exec -io ./ring``

``mpirun -np 8 tau_exec -ebs -ebs_period=1000000 -ebs_source=PAPI_FP_INS ./ring``

``tau_exec -T serial,cupti -cupti ./matmult (Preferred for CUDA 4.1 or later)``

``tau_exec -T serial -cuda ./matmult (Preferred for CUDA 4.0 or earlier)``

``tau_exec -T serial -opencl (OPENCL)``

tau\_timecorrect
1
tau\_timecorrect
Corrects and reorders the records of tau trace files.
tau\_timecorrect
trace input file
EDF input file
trace output file
EDF input file
Description
===========

This program takes in tau trace files, reorders and corrects the times
of these records and then outputs the records to new trace files. The
time correction algorithm uses a logical clock algorithm with
amortization. This is done by adjusting the times of events such that
the product of an effect happens after the cause of that effect.

Options
=======

``trace input file``

``EDF input file``

``trace output file``

``EDF output file``

tau\_throttle.sh
1
tau\_throttle.sh
This tool generates a selective instrumentation file (called
throttle.tau) from a program output that has "Disabling" messages.
tau\_throttle.sh
Description
===========

This tools will auto-generates a selective instrumenation file basied on
output from a program that has the profiling of some its functions
throttled.

tau\_portal.py
1
tau\_portal.py
This tool is design to interact with the TAU web portal
(http://tau.nic.uoregon.edu). There are commands for uploading or
downloading packed profile files form the TAU portal.
tau\_portal.py
-help
--help
command
options
argument
Description
===========

Each command will initate a transfer to profile data btween the TAU
portal and either the filesytem (to be stored as ppk file) or to a
PerfDMF database. See ``tau_portal --help`` for more information.

taudb\_configure
1
taudb\_configure
Configuration program for a PerfDMF database.
taudb\_configure
-h,--help
--create-default
-g, --configFile
configFile
-c, --config
configuration\_name
-t, --tauroot
path
Description
===========

This configuration script will create a new TAUdb database.

Options
=======

-h, --help show help

--create-default creates a H2 database with all the default values

-g, --configFile ``configFile `` specify the path to the file that
defines the TAUdb configuration.

-c, --config ``configuration_name `` specify the name of the TAUdb
configuration -c foo is equalivent to -g
``<home>/.ParaProf/perfdmf.cfg.foo``.

-t, --tauroot ``path `` Path to the root directory of tau.

perfdmf\_createapp
1
perfdmf\_createapp
Deprecated
Command line tool to create a application in the perfdmf database.
(Deprecated)
perfdmf\_createapp
-h, --help
-g, --configFile
configFile
-c, --config
configuration\_name
-a, --applicationid
applicationID
-n, --name
name
Description
===========

This script will create a new application in the perfdmf database.

Options
=======

-g, --configFile ``configFile `` specify the path to the file that
defines the perfdmf configuration.

-c, --config ``configuration_name `` specify the name of the perfdmf
configuration -c foo is equalivent to -g
``<home>/.ParaProf/perfdmf.cfg.foo``.

-a, --applicationid ``applicationID `` specify the id number of the
newly added application (default uses auto-increment).

-n, --name ``name `` the name of the application.

perfdmf\_createexp
1
perfdmf\_createexp
Deprecated
Command line tool to create a experiment in the perfdmf database.
(Deprecated)
perfdmf\_createexp
-h, --help
-g, --configFile
configFile
-c, --config
configuration\_name
-a, --applicationid
applicationID
-n, --name
name
Description
===========

This script will create a new experiment in the perfdmf database.

Options
=======

-g, --configFile ``configFile `` specify the path to the file that
defines the perfdmf configuration.

-c, --config ``configuration_name `` specify the name of the perfdmf
configuration -c foo is equalivent to -g
<home>/.ParaProf/perfdmf.cfg.foo.

-a, --applicationid ``applicationID `` specify the id number of the
application to associate with the new experiment.

-n, --name ``name `` the name of the application.

taudb\_loadtrial
1
taudb\_loadtrial
Command line tool to load a trial into the TAUdb database.
taudb\_loadtrial
-a
appName
-x
experimentName
-n
name
options
Description
===========

This script will create a new trial in the TAUdb database.

Options
=======

-n, --name ``name `` the name of the application.

-a, --applicationname `` name `` specify associated application name for
this trial

-x, --experimentname ``experimentName `` specify the name of the
experiment to associate with newly uploaded trial.

-e, --experimentid ``experimentID `` specify the id number of the
experiment to associate with the new trial.

-g, --configFile ``configFile `` specify the path to the file that
defines the TAUdb configuration. (overrides -c)

-c, --config ``configuration_name `` specify the name of the TAUdb
configuration -c foo is equalivent to -g <.

-t, --trialid ``experimentID `` specify the id number of the newly
uploaded trial.

-m, --metadata ``filename `` specify the filename of the XML metadata
for this trial.

-f, --filetype ``filetype`` Specify type of performance data, options
are: profiles (default), pprof, dynaprof, mpip, gprof, psrun, hpm,
packed, cube, hpc, ompp, snap, perixml, gptl, paraver, ipm, google

-i, --fixnames Use the fixnames option for gprof

Notes
=====

For the TAU profiles type, you can specify either a specific set of
profile files on the commandline, or you can specify a directory (by
default the current directory). The specified directory will be searched
for profile.\*.\*.\* files, or, in the case of multiple counters,
directories named MULTI\_\* containing profile data.

Examples
========

taudb\_loadtrial -e 12 -n "Batch 001"

This will load profile.\* (or multiple counters directories MULTI\_\*)
into experiment 12 and give the trial the name "Batch 001"

taudb\_loadtrial -e 12 -n "HPM data 01" -f hpm perfhpm\*

This will load perfhpm\* files of type HPMToolkit into experiment 12 and
give the trial the name "HPM data 01"

taudb\_loadtrial -a "NPB2.3" -x "parametric" -n "64" par64.ppk

This will load packed profile par64.ppk into the experiment named
"parametric" under the application named "NPB2.3" and give the trial the
name "64". The application and experiment will be created if not found.

perfexplorer
1
perfexplorer
Launches TAU's Performance Data Mining Analyzer.
perfexplorer
-n, --nogui
-i, --script
script
Documentation
=============

Complete documentation can be found at
*http://www.cs.uoregon.edu/research/tau/tau-usersguide.pdf*

perfexplorer\_configure
1
perfexplorer\_configure
Configures a TAUdb database for use with perfexplorer, and installs
necessary JAR files.
perfexplorer\_configure
Description
===========

Configures a TAUdb database for use with perfexplorer, and installs
necessary JAR files.

taucc
1
taucc
C compiler wrapper for TAU
taucc
options
...
Options
=======

``-tau:help``
    Displays help

``-tau:verbose``
    Enable verbose mode

``-tau:keepfiles``
    Keep intermediate files

``-tau:show``
    Do not invoke, just show what would be done

``-tau:pdtinst``
    Use PDT instrumentation

``-tau:compinst``
    Use compiler instrumentation

``-tau:headerinst``
    Instrument headers

``-tau:<options>``
    Specify measurement/instrumentation options. Sample options:
    mpi,pthread,openmp,profile,callpath,trace,vampirtrace,epilog

``-tau:makefile tau_stub_makefile``
    Specify tau stub makefile

Notes
=====

If the -tau:makefile option is not used, the TAU\_MAKEFILE environment
variable will be checked, if it is not specified, then the
-tau:<options> will be used to identify a binding.

Examples
========

taucc foo.c -o foo

taucc -tau:MPI,OPENMP,TRACE foo.c -o foo

taucc -tau:verbose -tau:PTHREAD foo.c -o foo

Documentation
=============

Complete documentation can be found at
*http://www.cs.uoregon.edu/research/tau/tau-usersguide.pdf*

tauupc
1
tauupc
UPC wrapper for TAU
tauupc
options
...
Options
=======

``-tau:help``
    Displays help

``-tau:verbose``
    Enable verbose mode

``-tau:keepfiles``
    Keep intermediate files

``-tau:show``
    Do not invoke, just show what would be done

``-tau:pdtinst``
    Use PDT instrumentation

``-tau:compinst``
    Use compiler instrumentation

``-tau:headerinst``
    Instrument headers

``-tau:<options>``
    Specify measurement/instrumentation options. Sample options:
    mpi,pthread,openmp,profile,callpath,trace,vampirtrace,epilog

``-tau:makefile tau_stub_makefile``
    Specify tau stub makefile

Notes
=====

If the -tau:makefile option is not used, the TAU\_MAKEFILE environment
variable will be checked, if it is not specified, then the
-tau:<options> will be used to identify a binding.

Documentation
=============

Complete documentation can be found at
*http://www.cs.uoregon.edu/research/tau/tau-usersguide.pdf*

taucxx
1
taucxx
C++ compiler wrapper for TAU
taucxx
options
...
Options
=======

``-tau:help``
    Displays help

``-tau:verbose``
    Enable verbose mode

``-tau:keepfiles``
    Keep intermediate files

``-tau:show``
    Do not invoke, just show what would be done

``-tau:pdtinst``
    Use PDT instrumentation

``-tau:compinst``
    Use compiler instrumentation

``-tau:headerinst``
    Instrument headers

``-tau:<options>``
    Specify measurement/instrumentation options. Sample options:
    mpi,pthread,openmp,profile,callpath,trace,vampirtrace,epilog

``-tau:makefile tau_stub_makefile``
    Specify tau stub makefile

Notes
=====

If the -tau:makefile option is not used, the TAU\_MAKEFILE environment
variable will be checked, if it is not specified, then the
-tau:<options> will be used to identify a binding.

Examples
========

taucxx foo.cpp -o foo

taucxx -tau:MPI,OPENMP,TRACE foo.cpp -o foo

taucxx -tau:verbose -tau:PTHREAD foo.cpp -o foo

Documentation
=============

Complete documentation can be found at
*http://www.cs.uoregon.edu/research/tau/tau-usersguide.pdf*

tauf90
1
tauf90
Fortran compiler wrapper for TAU
tauf90
options
...
Options
=======

``-tau:help``
    Displays help

``-tau:verbose``
    Enable verbose mode

``-tau:keepfiles``
    Keep intermediate files

``-tau:show``
    Do not invoke, just show what would be done

``-tau:pdtinst``
    Use PDT instrumentation

``-tau:compinst``
    Use compiler instrumentation

``-tau:headerinst``
    Instrument headers

``-tau:<options>``
    Specify measurement/instrumentation options. Sample options:
    mpi,pthread,openmp,profile,callpath,trace,vampirtrace,epilog

``-tau:makefile tau_stub_makefile``
    Specify tau stub makefile

Notes
=====

If the -tau:makefile option is not used, the TAU\_MAKEFILE environment
variable will be checked, if it is not specified, then the
-tau:<options> will be used to identify a binding.

Examples
========

tauf90 foo.f90 -o foo

tauf90 -tau:MPI,OPENMP,TRACE foo.f90 -o foo

tauf90 -tau:verbose -tau:PTHREAD foo.f90 -o foo

Documentation
=============

Complete documentation can be found at
*http://www.cs.uoregon.edu/research/tau/tau-usersguide.pdf*

paraprof
1
paraprof
Launches TAU's Java-based performance data viewer.
paraprof
-h, --help
-f, --filetype
filetype
--pack
file
--dump
-o, --oss
-s, --summary
Notes
=====

For the TAU profiles type, you can specify either a specific set of
profile files on the commandline, or you can specify a directory (by
default the current directory). The specified directory will be searched
for profile.\*.\*.\* files, or, in the case of multiple counters,
directories named MULTI\_\* containing profile data.

Options
=======

``-h``
    Display help

``-f, --filetype filetype``
    Specify type of performance data. Options are: profiles (default),
    pprof, dynaprof, mpip, gprof, psrun, hpm, packed, cube, hpc, ompp,
    snap, perixml, gptl

``--pack file``
    Pack the data into packed (.ppk) format (does not launch ParaProf
    GUI)

``--dump``
    Dump profile data to TAU profile format (does not launch ParaProf
    GUI).

``-o, --oss``
    Print profile data in OSS style text output

``-s, --summary``
    Print only summary statistics (only applies to OSS output)

Documentation
=============

Complete documentation can be found at
*http://www.cs.uoregon.edu/research/tau/tau-usersguide.pdf*

pprof
1
pprof
Quickly diplays profile data.
pprof
-a
-c
-b
-m
-t
-e
-i
-v
-r
-s
-n
num
-f
filename
-p
-l
-d
Description
===========

Options
=======

-a Show all location information available

-c Sort according to number of Calls

-b Sort according to number of suBroutines called by a function

-m Sort according to Milliseconds (exclusive time total)

-t Sort according to Total milliseconds (inclusive time total) (default)

-e Sort according to Exclusive time per call (msec/call)

-i Sort according to Inclusive time per call (total msec/call)

-v Sort according to Standard Deviation (excl usec)

-r Reverse sorting order

-s print only Summary profile information

-n num print only first num number of functions

-f filename specify full path and Filename without node ids

-p suPpress conversion to hhmmssmmm format

-l List all functions and exit

-d Dump output format (for tau\_reduce) [node numbers] prints only info
about all contexts/threads of given node numbers

tau\_instrumentor
1
tau\_instrumentor
automaticly instruments a source basied on information provided by pdt.
tau\_instrumentor
--help
pdbfile
sourcefile
-c
-b
-m
-t
-e
-i
-v
-r
-s
-n
num
-f
filename
-p
-l
-d
Description
===========

Options
=======

-a Show all location information available

-c Sort according to number of Calls

-b Sort according to number of suBroutines called by a function

-m Sort according to Milliseconds (exclusive time total)

-t Sort according to Total milliseconds (inclusive time total) (default)

-e Sort according to Exclusive time per call (msec/call)

-i Sort according to Inclusive time per call (total msec/call)

-v Sort according to Standard Deviation (excl usec)

-r Reverse sorting order

-s print only Summary profile information

-n num print only first num number of functions

-f filename specify full path and Filename without node ids

-p suPpress conversion to hhmmssmmm format

-l List all functions and exit

-d Dump output format (for tau\_reduce) [node numbers] prints only info
about all contexts/threads of given node numbers

Example
=======

``%> tau_instrumentor foo.pdb foo.cpp -o foo.inst.cpp -f
  select.tau``

vtfconverter
1
vtfconverter
vtfconverter
-h
-c
-f
file
-p
path
-i
from
to
Description
===========

Converts VTF profile to TAU profiles and launches an interactive VTF
prompt.

Options
=======

-c Opens command line interface.

-f Converts trace [file] to TAU profiles.

-p Places the resulting profiles in the directory [path].

-i States that the interval [from],[to] should be profiled.

tau\_setup
1
tau\_setup
Launches GUI interface to configure TAU.
tau\_setup
Options
=======

-v Verbose output.

--html Output results in HTML.

--build Only build.

--run Only run.

tau\_wrap
1
tau\_wrap
Instruments an external library with TAU without needing to recompile
tau\_wrap
pdbfile
sourcefile
-o
outputfile
-g
groupname
-i
headerfile
-f
selectivefile
Options
=======

pdbfile
    A pdb file generated by cparse, cxxparse, or f90parse; these
    commands are found in the [PDT\_HOME]/[arch]/bin directory.

sourcefile
    The source file corresponding to the pdbfile.

-o outputfile
    The filename of the resulting instrumented source file.

-g groupname
    This associates all the functions profiled as belonging to the this
    group. Once profiled you will be able to analysis these functions
    separately.

-i headerfile
    By default ``tau_wrap`` will include Profile/Profile.h; use this
    option to specify a different header file.

-f selectivefile
    You can specify a selective instrumentation file that defines how
    the source file is to be instrumented.

Examples
========

::

    %> tau_wrap hdf5.h.pdb hdf5.h -o hdf5.inst.c -f select.tau -g hdf5

This specifies the instrumented wrapper library source (hdf5.inst.c),
the instrumentation specification file (select.tau) and the group
(hdf5). It creates the wrapper/ directory.

tau\_gen\_wrapper
1
tau\_gen\_wrapper
Generates a wrapper library that can intercept at link time or at
runtime routines specified in a header file
tau\_gen\_wrapper
headerfile
library
-w \| -d \| -r
Options
=======

headerfile
    Name of the headerfile to be wrapped

library
    Name of the library to wrap

-w
    (default) generates wrappers for re-linking the application

-d
    generates wrappers by redefining routines during compilation in
    header files

-r
    generates wrappers that may be pre-loaded using tau\_exec at runtime

Examples
========

::

    %>  tau_gen_wrapper hdf5.h /usr/lib/libhdf5.a 

This generates a wrapper library that may be linked in using
TAU\_OPTIONS -optTauWrapFile=<wrapperdir>/link\_options.tau

Notes
=====

tau\_gen\_wrapper reads the TAU\_MAKEFILE environment variable to get
PDT settings

tau\_pin
1
tau\_pin
Instruments application at run time using Intel's PIN library
tau\_pin
-n
proc\_num
-r
rules
--
myapp
myargs
Options
=======

``-n`` ``proc_num``
    This argument enables multple instances of MPI applications launched
    with MPIEXEC. proc\_num is the parameter indicating number of MPI
    process instances to be launched. This argument is optional and one
    can profile MPI application even with single process instance
    without this argument.

``-r`` ``rule``
    This argument is specification rule for profiling the application.
    It allows selective profiling by specifying the "rule". The rule is
    a wildcard expression token which will indicate the area of
    profiling. It can be only the routine specification like "\*" which
    indicates it'll instrument all the routines in the EXE or MPI
    routines. One can further specify the routines on a particular dll
    by the rule "somedll.dll!\*". The dll name can also be in regular
    expression. We treat the application exe and MPI routines as special
    cases and specifying only the routines is allowed.

``myapp``
    It's the application exe. This application can be Windows or console
    application. Profiling large Windows applications might suffer from
    degraded performance and interactability. Specifying a limited
    number of interesting routines can help.

``myargs``
    It's the command line arguments of the application.

Examples
========

To profile routines in mytest.exe with prefix "myf":

::

    tau_pin -r myf.*  -- mytest.exe

To profile all routines in mpitest.exe ( no need to specify any rule for
all ):

::

    tau_pin  mpitest.exe

to profile only MPI routines in mpitest.exe by launching two instances:

::

    tau_pin -n 2 -r _MPI_.* -- mpitest.exe

Wildcards
---------

-  ``*`` for anything, for example \*MPI\* means any string having MPI
   in between any other characters.

-  ``?`` It's a placeholder wild card ?MPI\* means any character
   followed by MPI and followed by any string, example: ``??Try`` could
   be ``__Try`` or ``MyTry`` or ``MeTry`` etc.

tau\_java
1
tau\_java
Instruments java applications at runtime using JVMTI
tau\_java
options
javaprogram
args
Options
=======

```` ``-help``
    Displays help information.

```` ``-verbose``
    Report the arguments of the script before it runs.

```` ``-tau:agentlib=<agentlib>``
    By default tau\_java uses the most recently configured jdk, you can
    specify a different one here.

```` ``-tau:java=<javapath>``
    Path to a java binary, by default uses the one corresponding to the
    most recently configured jdk.

```` ``-tau:bootclasspath= <bootclasspath>``
    To modify the bootclasspath to point to a different jar, not usually
    necessary.

```` ``-tau:include=<item>``
    Only instrument these methods or classes. Separate multiple classes
    and methods with semicolons

``-tau:exclude=<item>``
    Exclude the listed classes and methods. Separate multiple classes
    and methods with semicolons

``args``
    the command line arguments of the java application.

tau\_cupti\_avail
1
tau\_cupti\_avail
Detects the available CUPTI counters on the a each GPU device.
tau\_cupti\_avail
-c
counter names
Options
=======

``-c`` ``counter names``
    Checks which of a colon seperated list of CUPTI counter names can be
    recorded.

tau\_run
1
tau\_run
Instruments and executes binaries to generate performance data.
(DyninstAPI based instrumentor)
Options
=======

``-v`` ````
    optional verbose option

``-o`` ``outfile``
    for binary rewriting

-T<option>
    : specify TAU option

-loadlib=<file.so >
    : specify additional load library

-XrunTAU-<options>
    specify TAU library directly

tau\_rewrite
1
tau\_rewrite
Rewrites binaries using Maqao if Tau is configured using PDT 3.17+ at
the routine level. If it doesn't find the Maqao package from PDT 3.17,
it reverts to tau\_run (DyninstAPI based instrumentor).
Options
=======

``-o`` ``outfile``
    specify instrumented output file

``-T`` ````
    specify TAU option (CUPTI, DISABLE, MPI, OPENMP, PDT, PGI, PROFILE,
    SCOREP, SERIAL)

``-loadlib=`` ``file.so``
    specify additional load library

``-s`` ````
    dryrun without executing

``-v`` ````
    long verbose mode

``-v1`` ````
    short verbose mode

``-XrunTAUsh-`` ``options``
    specify TAU library directly

Notes
=====

Defaults if unspecified: -T MPI

MPI is assumed unless SERIAL is specified

Example
=======

::

        
        tau_rewrite -T papi,pdt a.out -o a.inst

::

        mpirun -np 4 ./a.inst
