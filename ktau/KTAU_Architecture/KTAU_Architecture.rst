KTAU Architecture
=================

KTAU comprises 4 individual modules

-  - KTAU Instrumentation

-  - KTAU Infrastructure

-  - KTAU Proc Interface

-  - KTAU User-API Library and Utilities

KTAU Instrumentation
--------------------

KTAU places instrumentation points in Linux kernel source to intercept
the execution path and extract the performance data of interest. For
instance, KTAU places instrumentation at the entry and exit point of a
kernel routine to measure the amount of time spending inside the
routine. Time measurement is in tick, which is obtained from the
timestamp counter of a processor. Most Intel processors tick-rate is
normally equal to the clock speed of the processor, but varies on PPC.

For each function being instrumented, KTAU assigns a unique ID at
runtime. This ID is assigned dynamically depending on the order the
function was executed. It is assigned once at the first time a process
execute the function, and will be maintained as long as the system is
running. In other word, the ID is not bound to the function across the
system reboot. This ID is used as an index into a table, which stores
profile data of each function. This technique allows profile data to be
accessed directly with out searching through a list of functions.

KTAU Infrastructure
-------------------

KTAU main infrastructure resides in task\_struct of each process. It
consists of a profile table, a circular trace buffer, locks, and state
variables. The profile table is used to store profile data (i.e. amount
of time a process spent inside a function, counter, etc). The function
ID is used to index into the table. Currently, the table has 1,024
entries, which are grouped into ranges that adopt different indexing
schemes. Please refer to appendix A for more detail.

KTAU Proc Interface
-------------------

KTAU uses ``/proc`` filesystem as a communication channel between
kernel-space and user-space. ``/proc/ktau/profile`` and
``/proc/ktau/trace`` are used for accessing profile data and trace data
respectively. Generally, applications from user-space access the data
through provided user-API library, which uses ioctl as underlying
communication method.

KTAU User-API Library and Utilities
-----------------------------------

KTAU uses ``/proc`` filesystem as a communication channel between
kernel-space and user-space. "/proc/ktau/profile"and
``/proc/ktau/trace`` are used for accessing profile data and trace data
respectively. Generally, applications from user-space access the data
through provided user-API library, which uses ioctl as underlying
communication method.
