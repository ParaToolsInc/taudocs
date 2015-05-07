Quick Reference
===============

``tau_run``
    TAU's binary instrumentation tool
``tau_cc.sh -tau_options=-optCompInst / tau_cxx.sh -tau_options=-optCompInst / tau_f90.sh -tau_options=-optCompInst``
    Compiler wrappers
    (Compiler instrumentation)
``tau_cc.sh / tau_cxx.sh / tau_f90.sh``
    Compiler wrappers
    (PDT instrumentation)
``TAU_MAKEFILE``
    Set instrumentation definition file
``TAU_OPTIONS``
    Set instrumentation options
``dynamic phase name='name'
          file='filename'
            line=start_line_# to
            line=end_line_#    
            ``
    Specify dynamic Phase
``loops file='filename'
            routine='routine name' 
            ``
    Instrument outer loops
``memory file='filename'
            routine='routine name' 
            ``
    Track memory
``io file='filename'
            routine='routine name' 
            ``
    Track IO
``TAU_PROFILE / TAU_TRACE``
    Enable profiling and/or tracing
``PROFILEDIR / TRACEDIR``
    Set profile/trace output directory
``TAU_CALLPATH=1 / TAU_CALLPATH_DEPTH``
    Enable Callpath profiling, set callpath depth
``TAU_THROTTLE=1 / TAU_THROTTLE_NUMCALLS / TAU_THROTTLE_PERCALL``
    Enable event throttling, set number of call, percall (us) threshold
``TAU_METRICS``
    List of PAPI metrics to profile
``tau_treemerge.pl``
    Merge traces to one file
``tau2otf / tau2vtf / tau2slog2``
    Trace conversion tools
