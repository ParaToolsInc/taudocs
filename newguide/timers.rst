-  **Static timers**

   These are commonly used in most profilers where all invocations of a
   routine are recorded. The name and group registration takes place
   when the timer is created (typically the first time a routine is
   entered). A given timer is started and stopped at routine entry and
   exit points. A user defined timer can also measure the time spent in
   a group of statements. Timers may be nested but they may not overlap.
   The performance data generated can typically answer questions such
   as: *what is the total time spent in MPI\_Send() across all
   invocations?*

-  **Dynamic timers**

   To record the execution of each invocation of a routine, TAU provides
   dynamic timers where a unique name may be constructed for a dynamic
   timer for each iteration by embedding the iteration count in it. It
   uses the start/stop calls around the code to be examined, similar to
   static timers. The performance data generated can typically answer
   questions such as:\ *what is the time spent in the routine foo() in
   iterations 24, 25, and 40?*

-  **Static phases**

   An application typically goes through several phases in its
   execution. To track the performance of the application based on
   phases, TAU provides static and dynamic phase profiling. A profile
   based on phases highlights the context in which a routine is called.
   An application has a default phase within which other routines and
   phases are invoked. A phase based profile shows the time spent in a
   routine when it was in a given phase. So, if a set of instrumented
   routines are called directly or indirectly by a phase, we'd see the
   time spent in each of those routines under the given phase. Since
   phases may be nested, a routine may belong to only one phase. When
   more than one phase is active for a given routine, the closest
   ancestor phase of a routine along its callstack is its phase for that
   invocation. The performance data generated can answer questions such
   as: *what is the total time spent in MPI\_Send() when it was invoked
   in all invocations of the IO (IO => MPI\_Send()) phase?*

-  **Dynamic phases**

   Dynamic phases borrow from dynamic timers and static phases to create
   performance data for all routines that are invoked in a given
   invocation of a phase. If we instrument a routine as a dynamic phase,
   creating a unique name for each of its invocations (by embedding the
   invocation count in the name), we can examine the time spent in all
   routines and child phases invoked directly or indirectly from the
   given phase. The performance data generated can typically answer
   questions such as: *what is the total time spent in MPI\_Send() when
   it was invoked directly or indirectly in iteration 24?* Dynamic
   phases are useful for tracking per-iteration profiles for an adaptive
   computation where iterations may differ in their execution times.

-  **Callpaths**

   In phase-based profiles, we see the relationship between routines and
   parent phases. Phase profiles do not show the calling structure
   between different routines as is represented in a callgraph. To do
   so, TAU provides callpath profiling capabilities where the time spent
   in a routine along an edge of a callgraph is captured. Callpath
   profiles present the full flat profiles of routines (or nodes in the
   callgraph), as well as routines along a callpath. A callpath is
   represented syntactically as a list of routines separated by a
   delimiter. The maximum depth of a callpath is controlled by an
   environment variable.

-  **User-defined Events**

   Besides timers and phases that measure the time spent between a pair
   of start and stop calls in the code, TAU also provides support for
   user-defined atomic events. After an event is registered with a name,
   it may be triggered with a value at a given point in the source code.
   At the application level, we can use user-defined events to track the
   progress of the simulation by keeping track of application specific
   parameters that explain program dynamics, for example, the number of
   iterations required for convergence of a solver at each time step, or
   the number of cells in each iteration of an adaptive mesh refinement
   application.
