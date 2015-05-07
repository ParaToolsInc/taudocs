Introduction
============

ParaProf is a portable, scalable performance analysis tool included with
the TAU distribution.

    **Important**

    ParaProf requires *Oracle / Sun's* Java 1.5 Runtime Environment for
    basic functionality. Java JOGL (included) is required for 3d
    visualization and image export. Additionally, OpenGL is required for
    3d visualization.

    **Note**

    Most windows in ParaProf can export bitmap (png/jpg) and vector
    (svg/eps) images to disk (png/jpg) or print directly to a printer.
    This are available through the *File* menu.

Using ParaProf from the command line
====================================

ParaProf is a java program that is run from the supplied ``paraprof``
script (``paraprof.bat`` for windows binary release).

::

    % paraprof --help
    Usage: paraprof [options] <files/directory>

    Options:

      -f, --filetype <filetype>       Specify type of performance data, options are:
                                        profiles (default), pprof, dynaprof, mpip,
                                        gprof, psrun, hpm, packed, cube, hpc, ompp
                                        snap, perixml, gptl, ipm, google
      --range a-b:c                   Load only profiles from the given range(s) of processes
                                        Seperate individual ids or dash-defined ranges with colons
      -h, --help                      Display this help message

    The following options will run only from the console (no GUI will launch):

      --merge <file.gz>               Merges snapshot profiles
      --pack <file>                   Pack the data into packed (.ppk) format
      --dump                          Dump profile data to TAU profile format
      --dumprank <rank>               Dump profile data for <rank> to TAU profile format
      -v, --dumpsummary               Dump derived statistical data to TAU profile format
      --overwrite                     Allow overwriting of profiles
      -o, --oss                       Print profile data in OSS style text output
      -q, --dumpmpisummary            Print high level time and communication summary
      -d, --metadump                  Print profile metadata (works with --dumpmpisummary)
      -x, --suppressmetrics           Exclude child calls and exclusive time from --dumpmpisummary
      -s, --summary                   Print only summary statistics
                                        (only applies to OSS output)

    Notes:
      For the TAU profiles type, you can specify either a specific set of profile
    files on the commandline, or you can specify a directory (by default the current
    directory).  The specified directory will be searched for profile.*.*.* files,
    or, in the case of multiple counters, directories named MULTI_* containing
    profile data.

Supported Formats
=================

ParaProf can load profile date from many sources. The types currently
supported are:

Command line options
====================

In addition to specifying the profile format, the user can also specify
the following options

-  **--fixnames** - Use the fixnames option for gprof. When C and
   Fortran code are mixed, the C routines have to be mapped to either
   .function or function\_. Strip the leading period or trailing
   underscore, if it is there.

-  **--pack <file>** - Rather than load the data and launch the GUI,
   pack the data into the specified file.

-  **--dump** - Rather than load the data and launch the GUI, dump the
   data to TAU Profiles. This can be used to convert supported formats
   to TAU Profiles.

-  **--oss** - Outputs profile data in OSS Style. Example:

   ::

       -------------------------------------------------------------------------------
       Thread: n,c,t 0,0,0
       -------------------------------------------------------------------------------
        excl.secs  excl.%   cum.%    PAPI_TOT_CYC     PAPI_FP_OPS     calls  function
            0.005   56.0%   56.0%        13475345         4194518         1  foo
            0.003   40.1%   96.1%         9682185         4205367         1  bar
                0    3.6%   99.7%          223173           17445         1  baz
          2.2E-05    0.3%  100.0%           14663             206         1  main

-  **--summary** - Output only summary information for OSS style output.
