-  **TAU Profiles (profiles)** - Output from the TAU measurement
   library, these files generally take the form of ``profile.X.X.X``,
   one for each node/context/thread combination. When multiple counters
   are used, each metric is located in a directory prefixed with
   "MULTI\_\_". To launch ParaProf with all the metrics, simply launch
   it from the root of the MULTI\_\_ directories.

-  **ParaProf Packed Format (ppk)** - Export format supported by
   PerfDMF/ParaProf. Typically .ppk.

-  **TAU Merged Profiles (snap)** - Merged and snapshot profile format
   supported by TAU. Typically tauprofile.xml.

-  **TAU pprof (pprof)** - Dump Output from TAU's ``pprof -d``. Provided
   for backward compatibility only.

-  **DynaProf (dynaprof)** - Output From DynaProf's wallclock and papi
   probes.

-  **mpiP (mpip)** - Output from mpiP.

-  **gprof (gprof)** - Output from gprof, see also the --fixnames
   option.

-  **PerfSuite (psrun)** - Output from PerfSuite psrun files.

-  **HPM Toolkit (hpm)** - Output from IBM's HPM Toolkit.

-  **Cube (cube)** - Output from Kojak Expert tool for use with Cube.

-  **Cube3 (cube3)** - Output from Kojak Expert tool for use with Cube3
   and Cube4.

-  **HPCToolkit (hpc)** - XML data from hpcquick. Typically, the user
   runs hpcrun, then hpcquick on the resulting binary file.

-  **OpenMP Profiler (ompp)** - CSV format from the ompP OpenMP Profiler
   (http://www.ompp-tool.com). The user must use OMPP\_OUTFORMAT=CVS.

-  **PERI XML (perixml)** - Output from the PERI data exchange format.

-  **General Purpose Timing Library (gptl)** - Output from the General
   Purpose Timing Library.

-  **Paraver (paraver)** - 2D output from the Paraver trace analysis
   tool from BSC.

-  **IPM (ipm)** - Integrated Performance Monitoring format, from NERSC.

-  **Google (google)** - Google Profiles.
