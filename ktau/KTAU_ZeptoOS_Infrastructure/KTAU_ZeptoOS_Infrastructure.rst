KTAU Infrastructure for ANL BlueGene/L System
=============================================

KTAU and ZeptoOS Overview
-------------------------

NOTE: More detail information of ANL BluGene/L system configuration can
be found at http://www.bgl.mcs.anl.gov/bgl/.

One of KTAU's goals is to provide kernel profiling/tracing facility for
application running on BG/L system. On a Linux system, KTAU can be used
to monitor kernel activities among processes. At compile time, user can
enable sets of instrumentations which target different features of Linux
kernel such as system calls, TCP stacks, interrup handling, bottomhalf
handling, and etc. KTAU can genarate profile/trace for system-wide (all
running processes) or individual process, which can be viewed using
existing tools such as Paraprof for profile, and Vampir or Jumpshot for
trace. Since BG/L uses a modified version of Linux as io-node kernel,
this allows KTAU to be able to profile/trace kernel activities of the
io-node with little modification.

In order to run KTAU on BG/L, KTAU is loosely integrated as part of
`ZeptoOS <http://www-unix.mcs.anl.gov/zeptoos/>`__. ZeptoOS is a set of
utilities that allow users to configure the environment for running jobs
on BG/L. This includes specifying kernel image for io-node and
compute-node, ramdisk image , filesystem, remote-login facility using
ssh and telnet, and etc. Users can download
`KTAU <http://www.cs.uoregon.edu/research/ktau/downloads.php>`__,
configure ZeptoOS to enable supports and specify parameters for KTAU,
build ZeptoOS, and then specify the built environment with the job
submission.

KTAU Framework
--------------

KTAU has two possible frameworks :

1. Daemon-based

   In this framework, we use KTAUD (KTAU daemon) to periodically access
   kernel profile/trace data and output to filesystem for
   post-processing. This framework allows KTAU to profile/trace any
   processes without instrumenting the source code. This is important in
   the case of BG/L where most source code is not available such as CIOD
   and other daemon processes.

2. Application-based

   Applications can explicitly call to KTAU User-APIs to access
   profile/trace data at any points. This framework requires that the
   application source code is available, and is instrumented with calls
   to access KTAU profile/trace data. An example is to instrument an
   application functions at the entry and exit points. This way, we can
   monitor how much kernel activities are present within each of the
   instrumented function. TAU uses this framework to access kenel-level
   profile/trace, which later can be merged with its own profile/trace
   from application-level. This results in a complete profile/trace
   information across the kernel-user space. This framework can be used
   on BG/L once the source code of CIOD or ZIOD (ZeptoOS version of
   CIOD) is available.

Current Infrastructure
----------------------

Currently, we use the daemon-based framework on BGL. KTAUD is included
to the ZeptoOS ramdisk image through the ZeptoOS configuration. KTAUD is
then started on the io-node during system initialization. It will run
until the job is finished, then terminated. We are able to monitor
process activities inside the kernel of ionode. An interesting example
is to monitor CIOD handling system calls forwarding from BG/L
compute-node. Please, see the `KTAU-ZeptoOS
Demos <http://www.cs.uoregon.edu/research/ktau/docs.php>`__ for more
details.
