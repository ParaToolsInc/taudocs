TAU scripted compilation
========================

If you wish to avoid the use of Makefiles altogether, TAU provides three
script that will instrument your code from the command line.

Usage
-----

TAU provides these scripts: tau\_f90.sh, tau\_cc.sh, and tau\_cxx.sh to
compile Fortan, C, and C++ programs respectively. These can the found in
the tools/src/ directory so you may wish to add it to your path. You
might use tau\_cc.sh to compile a C program by typing:

::

    %>tau_cc.sh -tau_makefile=[path to makefile] sampleCprogram.c

The Makefile can usually be found in the /[arch]/lib directory, for
example ``/apple/lib/Makefile.tau-pdt``.

Tau\_cc.sh also has the ability to use a Makefile specified in an
environment variable. to run tau\_cc.sh so it uses the Makefile
specified by environment variable ``TAU_MAKEFILE``, type:

::

    %>export TAU_MAKEFILE=[path to tau]/[arch]/lib/[makefile].
    %>tau_cc.sh sampleCprogram.c

Similarly, if you want to set tau option like selective instrumentation
use the ``TAU_OPTIONS`` environment variable.

Reference
---------

A complete list of option for these scripts:

::

                                                                                 
    -optVerbose
    Turn on verbose debugging message
    -optPdtDir=""                 
    PDT architecture directory. Typically $(PDTDIR)/$(PDTARCHDIR)
    -optPdtF95Opts=""             
    Options for Fortran parser in PDT (f95parse)
    -optPdtF95Reset=""            
    Reset options to the Fortran parser to the given list
    -optPdtCOpts=""               
    Options for C parser in PDT (cparse). Typically $(TAU_MPI_INCLUDE) $(TAU_INCLUDE) $(TAU_DEFS)
    -optPdtCReset=""              
    Reset options to the C parser to the given list
    -optPdtCxxOpts=""
    Options for C++ parser in PDT (cxxparse). Typically $(TAU_MPI_INCLUDE) $(TAU_INCLUDE) $(TAU_DEFS)
    -optPdtCReset=""              
    Reset options to the C++ parser to the given list
    -optPdtF90Parser=""           
    Specify a different Fortran parser. For e.g., f90parse instead of f95parse
    -optPdtUser=""                
    Optional arguments for parsing source code
    -optTauInstr=""               
    Specify location of tau_instrumentor. Typically $(TAUROOT)/$(CONFIG_ARCH)/bin/tau_instrumentor
    -optTauSelectFile=""          
    Specify selective instrumentation file for tau_instrumentor
    -optPDBFile=""                
    Specify PDB file for tau_instrumentor. Skips parsing stage.
    -optTau=""                    
    Specify options for tau_instrumentor
    -optCompile=""                
    Options passed to the compiler. Typically $(TAU_MPI_INCLUDE) $(TAU_INCLUDE) $(TAU_DEFS)
    -optReset=""                  
    Reset options to the compiler to the given list
    -optLinking=""                
    Options passed to the linker. Typically $(TAU_MPI_FLIBS) $(TAU_LIBS) $(TAU_CXXLIBS)
    -optLinkReset=""              
    Reset options to the linker to the given list
    -optTauCC="<cc>"
    Specifies the C compiler used by TAU
    -optOpariTool="<path/opari7>"  
    Specifies the location of the Opari tool
    -optOpariDir="<path>"
    Specifies the location of the Opari directory
    -optOpariOpts=""              
    Specifies optional arguments to the Opari tool
    -optOpariReset=""             
    Resets options passed to the Opari tool
    -optNoMpi                     
    Removes -l*mpi* libraries during linking (default)
    -optMpi                       
    Does not remove -l*mpi* libraries during linking
    -optKeepFiles
    Does not remove intermediate .pdb and .inst.* files

