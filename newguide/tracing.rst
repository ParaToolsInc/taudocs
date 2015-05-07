Tracing
=======

Typically, profiling shows the distribution of execution time across
routines. It can show the code locations associated with specific
bottlenecks, but it can not show the temporal aspect of performance
variations. Tracing the execution of a parallel program shows when and
where an event occurred, in terms of the process that executed it and
the location in the source code. This chapter discusses how TAU can be
used to generate event traces.

Generating Event Traces
=======================

To enable tracing with TAU, set the environment variable ``TAU_TRACE``
to 1. Similarly you can enable/disable profile with the ``TAU_PROFILE``
variable. Just like with profiling, you can set the output directory
with a environment variable:

::

    % setenv TRACEDIR /users/sameer/tracedata/experiment56

This will generate a trace file and an event file for each processor. To
merge these files, use the ``tau_treemerge.pl`` script. If you want to
convert TAU trace file into another format use the ``tau2otf``,
``tau2vtf``, or ``tau2slog2`` scripts.
