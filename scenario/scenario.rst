Some Common Application Scenario
================================

Q. What routines account for the most time? How much?
=====================================================

A. Create a flat profile with wallclock time.

|Flat Profile|

::

    % setenv TAU_MAKEFILE /opt/apps/tau/tau-2.17.1/x86_64/lib/Makefile.tau-mpi-pdt-pgi
     
    % set path=(/opt/apps/tau/tau-2.17.1/x86_64/bin $path)
    % make F90=tau_f90.sh
    (Or edit Makefile and change F90=tau_f90.sh)
    % qsub  run.job
    % paraprof -–pack app.ppk
        Move the app.ppk file to your desktop. 

    % paraprof app.ppk

Q. What loops account for the most time? How much?
==================================================

A. Create a flat profile with wallclock time with loop instrumentation.

|Flat Profile with Loops|

::

    % setenv TAU_MAKEFILE /opt/apps/tau/tau-2.17.1/x86_64/lib/Makefile.tau-mpi-pdt
    % setenv TAU_OPTIONS ‘-optTauSelectFile=select.tau –optVerbose’
    % cat select.tau
      BEGIN_INSTRUMENT_SECTION
      loops routine=“#”
      END_INSTRUMENT_SECTION

    % set path=(/opt/apps/tau/tau-2.17.1/x86_64/bin $path)
    % make F90=tau_f90.sh
    (Or edit Makefile and change F90=tau_f90.sh)
    % qsub  run.job
    % paraprof -–pack app.ppk
        Move the app.ppk file to your desktop. 

    % paraprof app.ppk

Q. What MFlops am I getting in all loops?
=========================================

A. Create a flat profile with PAPI\_FP\_INS/OPS and time with loop
instrumentation.

|MFlops per loop|

::

    % setenv TAU_MAKEFILE /opt/apps/tau/tau-2.17.1/x86_64/lib/Makefile.tau-papi-mpi-pdt-pgi
    % setenv TAU_OPTIONS ‘-optTauSelectFile=select.tau –optVerbose’
    % cat select.tau
      BEGIN_INSTRUMENT_SECTION
      loops routine=“#”
      END_INSTRUMENT_SECTION

    % set path=(/opt/apps/tau/tau-2.17.1/x86_64/bin $path)
    % make F90=tau_f90.sh
    (Or edit Makefile and change F90=tau_f90.sh)
    % setenv TAU_METRICS GET_TIME_OF_DAY\:PAPI_FP_INS
    % qsub  run.job
    % paraprof -–pack app.ppk
        Move the app.ppk file to your desktop. 
    % paraprof app.ppk
      Choose 'Options' -> 'Show Derived Panel' -> Arg 1 = PAPI_FP_INS, Arg 2 =
        GET_TIME_OF_DAY, Operation = Divide -> Apply, close.

Q. Who calls MPI\_Barrier() Where?
==================================

A. Create a callpath profile with given depth.

|Callpath Profile|

::

    % setenv TAU_MAKEFILE
    % /opt/apps/tau/tau-2.17.1/x86_64/lib/Makefile.tau-mpi-pdt
    % set path=(/opt/apps/tau/tau-2.17.1/x86_64/bin $path)
    % make F90=tau_f90.sh
    (Or edit Makefile and change F90=tau_f90.sh)
    % setenv TAU_CALLPATH 1
    % setenv TAU_CALLPATH_DEPTH 100

    % qsub  run.job
    % paraprof -–pack app.ppk
        Move the app.ppk file to your desktop. 
    % paraprof app.ppk
    (Windows -> Thread -> Call Graph)

Q. How do I instrument Python Code?
===================================

A. Create an python wrapper library.

::

    % setenv TAU_MAKEFILE /opt/apps/tau/tau-2.17.1/x86_64/lib/Makefile.tau-icpc-python-mpi-pdt
    % set path=(/opt/apps/tau/tau-2.17.1/x86_64/bin $path)
    % setenv TAU_OPTIONS ‘-optShared -optVerbose'
    (Python needs shared object based TAU library)
    % make F90=tau_f90.sh CXX=tau_cxx.sh CC=tau_cc.sh  (build pyMPI w/TAU)
    % cat wrapper.py
      import tau
      def OurMain():
          import App
      tau.run(‘OurMain()’)
    Uninstrumented:
    % mpirun.lsf /pyMPI-2.4b4/bin/pyMPI ./App.py
    Instrumented:
    % setenv PYTHONPATH<taudir>/x86_64/<lib>/bindings-python-mpi-pdt-pgi
    (same options string as TAU_MAKEFILE)
    setenv LD_LIBRARY_PATH <taudir>/x86_64/lib/bindings-icpc-python-mpi-pdt-pgi\:$LD_LIBRARY_PATH
    % mpirun –np 4 <dir>/pyMPI-2.4b4-TAU/bin/pyMPI ./wrapper.py
    (Instrumented pyMPI with wrapper.py)

Q. What happens in my code at a given time?
===========================================

A. Create an event trace.

|Tracing with Vampir|

::

    % setenv TAU_MAKEFILE
    % /opt/apps/tau/tau-2.17.1/x86_64/lib/Makefile.tau-mpi-pdt-pgi
    % set path=(/opt/apps/tau/tau-2.17.1/x86_64/bin $path)
    % make F90=tau_f90.sh
    (Or edit Makefile and change F90=tau_f90.sh)
    % setenv TAU_TRACE 1
    % qsub  run.job
    % tau_treemerge.pl
    (merges binary traces to create tau.trc and tau.edf files)
    JUMPSHOT:
    % tau2slog2 tau.trc tau.edf –o app.slog2 
    % jumpshot app.slog2
       OR
    VAMPIR:
    % tau2otf tau.trc tau.edf app.otf –n 4 –z
    (4 streams, compressed output trace)
    % vampir app.otf
    (or vng client with vngd server).

Q. How does my application scale?
=================================

A. Examine profiles in PerfExplorer.

|Scalability chart|

::

    % setenv TAU_MAKEFILE /opt/apps/tau/tau-2.17.1/x86_64/lib/Makefile.tau-mpi-pdt
    % set path=(/opt/apps/tau/tau-2.17.1/x86_64/bin $path)
    % make F90=tau_f90.sh
    (Or edit Makefile and change F90=tau_f90.sh)
    % qsub  run1p.job
    % paraprof -–pack 1p.ppk
    % qsub run2p.job 
    % paraprof -–pack 2p.ppk ...and so on.
    On your client:
    % perfdmf_configure
    (Choose derby, blank user/password, yes to save password, defaults)
    % perfexplorer_configure
    (Yes to load schema, defaults)
    % paraprof 
    (load each trial: Right click on trial ->Upload trial to DB
    % perfexplorer 
    (Charts -> Speedup)

.. |Flat Profile| image:: flat_profile.png
.. |Flat Profile with Loops| image:: loop_profile.png
.. |MFlops per loop| image:: mflops_profile.png
.. |Callpath Profile| image:: callpath_profile.png
.. |Tracing with Vampir| image:: vampir_trace.png
.. |Scalability chart| image:: scalability.png
