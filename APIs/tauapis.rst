-  **C++**

   The C++ API is a set of macros that can be inserted in the C++ source
   code. An extension of the same API is available to instrument C and
   Fortran sources.

   At the beginning of each instrumented source file, include the
   following header

   ::

       #include <TAU.h>
           

-  **C**

   The API for instrumenting C source code is similar to the C++ API.
   The primary difference is that the ``TAU_PROFILE()`` macro is not
   available for identifying an entire block of code or function.
   Instead, routine transitions are explicitly specified using
   ``TAU_PROFILE_TIMER()`` macro with ``TAU_PROFILE_START()`` and
   ``TAU_PROFILE_STOP()`` macros to indicate the entry and exit from a
   routine. Note that, ``TAU_TYPE_STRING()`` and CT() macros are not
   applicable for C. It is important to declare the
   ``TAU_PROFILE_TIMER()`` macro after all the variables have been
   declared in the function and before the execution of the first C
   statement.

   Example:

   ::


       #include <TAU.h>

       int main (int argc, char **argv) {
         int ret;
         pthread_attr_t  attr;
         pthread_t       tid;
         TAU_PROFILE_TIMER(tautimer,"main()", "int (int, char **)",
                           TAU_DEFAULT);
         TAU_PROFILE_START(tautimer);
         TAU_PROFILE_INIT(argc, argv);
         TAU_PROFILE_SET_NODE(0);
         pthread_attr_init(&attr);
         printf("Started Main...\n");
         // other statements
         TAU_PROFILE_STOP(tautimer);
         return 0;
       }
             

-  **Fortran 77/90/95**

   The Fortran90 TAU API allows source code written in Fortran to be
   instrumented for TAU. This API is comprised of Fortran routines. As
   explained in Chapter 2, the instrumentation can be disabled in the
   program by using the TAU stub makefile variable ``TAU_DISABLE`` on
   the link command line. This points to a library that contains empty
   TAU instrumentation routines.

TAU\_START
3
TAU\_START
Starts a timer.
C/C++:
TAU\_START
char\*
name
Fortran:
TAU\_START
character
name
(2)
Description
===========

Starts the timer given by ``name``

Example
=======

**C/C++ :**

::

    int foo(int a) {
      TAU_START("t1");
      ...
      TAU_STOP("t2");
      return a;
    }
        

**Fortran :**

::

    subroutine F1()
      character(13) cvar

      write (cvar,'(a9,i2)') 'Iteration', val
      
        call TAU_START(cvar)
      ...
      call TAU_STOP(cvar)
    end
      

See Also
========

?, ?

TAU\_STOP
3
TAU\_STOP
Stops a timer.
C/C++:
TAU\_STOP
char\*
name
Fortran:
TAU\_STOP
character
name
(2)
Description
===========

Stops the timer given by ``timer``. It is important to note that timers
can be nested, but not overlapping. TAU detects programming errors that
lead to such overlaps at runtime, and prints a warning message.

Example
=======

**C/C++ :**

::

    int foo(int a) {
      TAU_START("t1");
      ...
      TAU_STOP("t2");
      return a;
    }
        

**Fortran :**

::

    subroutine F1()
      character(13) cvar

      write (cvar,'(a9,i2)') 'Iteration', val
      call TAU_START(cvar)
      ...
      call TAU_STOP(cvar)
    end
      

See Also
========

?, ?

TAU\_PROFILE
TAU\_PROFILE
Profile a C++ function
TAU\_PROFILE
char\* or string&
function\_name
char\* or string&
type
TauGroup\_t
group
Description
===========

``TAU_PROFILE`` profiles a function. This macro defines the function and
takes care of the timer start and stop as well. The timer will stop when
the macro goes out of scope (as in C++ destruction).

Example
=======

::

    int foo(char *str) {
      TAU_PROFILE(foo","int (char *)",TAU_DEFAULT);
      ...
    }
        

See Also
========

?

TAU\_DYNAMIC\_PROFILE
TAU\_DYNAMIC\_PROFILE
dynamic\_profile a c++ function
TAU\_DYNAMIC\_PROFILE
char\* or string&
function\_name
char\* or string&
type
taugroup\_t
group
description
===========

``TAU_DYNAMIC_PROFILE`` profiles a function dynamically creating a
separate profile for each time the function is called. this macro
defines the function and takes care of the timer start and stop as well.
the timer will stop when the macro goes out of scope (as in c++
destruction).

example
=======

::

    int foo(char *str) {
      tau_dynamic_profile("foo","int (char *)",tau_default);
      ...
    }
        

TAU\_PROFILE\_CREATE\_DYNAMIC
TAU\_PROFILE\_CREATE\_DYNAMIC
Creates a dynamic timer
C/C++:
TAU\_PROFILE\_CREATE\_DYNAMIC
Timer
timer
char\* or string&
function\_name
char\* or string&
type
taugroup\_t
group
Fortran:
TAU\_PROFILE\_CREATE\_DYNAMIC
integer
timer
(2)
character
name
(size)
description
===========

``TAU_PROFILE_CREATE_DYNAMIC`` creates a dynamic timer the name of the
timer should be different for each execution.

example
=======

>\ **C/C++:**

::

    int main(int argc, char **argv) {
      int i;
      TAU_PROFILE_TIMER(t,"main()", "", TAU_DEFAULT);
      TAU_PROFILE_SET_NODE(0);
      TAU_PROFILE_START(t);

      for (i=0; i&5; i++) {
        char buf[32];
        sprintf(buf, "Iteration %d", i);

        TAU_PROFILE_CREATE_DYNAMIC(timer, buf, "", TAU_USER);
        TAU_PROFILE_START(timer);
        printf("Iteration %d\n", i);
        f1();

        TAU_PROFILE_STOP(timer);
      }
      return 0;
    }

>\ **Fortran:**

::

     subroutine ITERATION(val)
      integer val
      character(13) cvar
      integer profiler(2) / 0, 0 /
      save profiler

      print *, "Iteration ", val

      write (cvar,'(a9,i2)') 'Iteration', val
      call TAU_PROFILE_CREATE_DYNAMIC(profiler, cvar)
      call TAU_PROFILE_START(profiler)

      call F1()
      call TAU_PROFILE_STOP(profiler)
      return
    end

see also
========

?

?

TAU\_CREATE\_DYNAMIC\_AUTO
TAU\_CREATE\_DYNAMIC\_AUTO
Creates a dynamic timer for C/C++
TAU\_CREATE\_DYNAMIC\_AUTO
Timer
timer
char\* or string&
function\_name
char\* or string&
type
taugroup\_t
group
description
===========

``TAU_CREATE_DYNAMIC_AUTO`` creates a dynamic timer automatically
incrementing the name each time the timer is executed.

example
=======

::

    int tau_ret_val;
    TAU_PROFILE_CREATE_DYNAMIC_AUTO(tautimer, "int foo1(int) C [{foo.c} {22,1}-{29,1}]", " ",TAU_USER);
    TAU_PROFILE_START(tautimer);
    {
    printf("inside foo1: calling bar: x = %d\n", x);
    printf("before calling bar in foo1\n");
    bar(x-1); /* 26 */
    printf("after calling bar in foo1\n");
    { tau_ret_val =  x; TAU_PROFILE_STOP(tautimer); return (tau_ret_val); }

see also
========

?

?

?

TAU\_PROFILE\_DYNAMIC\_ITER
TAU\_PROFILE\_DYNAMIC\_ITER
Creates a dynamic timer in Fortran.
TAU\_PROFILE\_DYNAMIC\_ITER
integer
iterator
integer
timer
(2)
character
name
(size)
description
===========

``TAU_PROFILE_DYNAMIC_ITER`` creates a dynamic timer the name of the
timer is appended by the iterator.

example
=======

::

      integer tau_iter / 0 /
      save tau_iter
      tau_iter = tau_iter + 1
      call TAU_PROFILE_DYNAMIC_ITER(tau_iter, profiler, '               &
     &FOO1 [{foo.f90} {16,18}]')
      call TAU_PROFILE_START(profiler)
      print *, "inside foo1: calling bar, x = ", x
      call bar(x-1)
      print *, "after calling bar"
      call TAU_PROFILE_STOP(profiler)

see also
========

?

?

TAU\_PHASE\_DYNAMIC\_ITER
TAU\_PHASE\_DYNAMIC\_ITER
Creates a dynamic phase in Fortran.
TAU\_PHASE\_DYNAMIC\_ITER
integer
iterator
integer
timer
(2)
character
name
(size)
description
===========

``TAU_PHASE_DYNAMIC_ITER`` creates a dynamic phase the name of which is
appended by the iterator.

example
=======

::

              integer tau_iter / 0 /
      save tau_iter
      tau_iter = tau_iter + 1
      call TAU_PHASE_DYNAMIC_ITER(tau_iter, profiler, '                 &
     &FOO1 [{foo.f90} {16,18}]')
      call TAU_PHASE_START(profiler)
      print *, "inside foo1: calling bar, x = ", x
      call bar(x-1)
      print *, "after calling bar"
      call TAU_PROFILE_STOP(profiler)

see also
========

?

?

TAU\_PROFILE\_TIMER
3
TAU\_PROFILE\_TIMER
Defines a static timer.
C/C++:
TAU\_PROFILE\_TIMER
Profiler
timer
char\* or string&
function\_name
char\* or string&
type
TauGroup\_t
group
Fortran:
TAU\_PROFILE\_TIMER
integer
profiler
(2)
character
name
(size)
Description
===========

**C/C++ :**

With ``TAU_PROFILE_TIMER``, a group of one or more statements is
profiled. This macro has a timer variable as its first argument, and
then strings for name and type, as described earlier. It associates the
timer to the profile group specified in the last parameter.

**Fortran :**

To profile a block of Fortran code, such as a function, subroutine, loop
etc., the user must first declare a profiler, which is an integer array
of two elements (pointer) with the save attribute, and pass it as the
first parameter to the ``TAU_PROFILE_TIMER`` subroutine. The second
parameter must contain the name of the routine, which is enclosed in a
single quote. ``TAU_PROFILE_TIMER`` declares the profiler that must be
used to profile a block of code. The profiler is used to profile the
statements using ``TAU_PROFILE_START`` and ``TAU_PROFILE_STOP`` as
explained later.

Example
=======

**C/C++ :**

::

    template< class T, unsigned Dim >
    void BareField<T,Dim>::fillGuardCells(bool reallyFill)
    {y
     // profiling macros
     TAU_TYPE_STRING(taustr, CT(*this) + " void (bool)" );
     TAU_PROFILE("BareField::fillGuardCells()", taustr, TAU_FIELD);
     TAU_PROFILE_TIMER(sendtimer, "fillGuardCells-send", 
                       taustr, TAU_FIELD);
     TAU_PROFILE_TIMER(localstimer, "fillGuardCells-locals",
                       taustr, TAU_FIELD);
     ...
    }
        

**Fortran :**

::

    subroutine bcast_inputs
    implicit none
    integer profiler(2)
    save profiler
                        
    include 'mpinpb.h'
    include 'applu.incl'
                        
    interger IERR
                        
    call TAU_PROFILE_TIMER(profiler, 'bcast_inputs')
      

See Also
========

?, ?, ?

TAU\_PROFILE\_START
3
TAU\_PROFILE\_START
Starts a timer.
C/C++:
TAU\_PROFILE\_START
Profiler
timer
Fortran:
TAU\_PROFILE\_START
integer
profiler
(2)
Description
===========

Starts the timer given by ``timer``

Example
=======

**C/C++ :**

::

    int foo(int a) {
      TAU_PROFILE_TIMER(timer, "foo", "int (int)", TAU_USER);
      TAU_PROFILE_START(timer);
      ...
      TAU_PROFILE_STOP(timer);
      return a;
    }
        

**Fortran :**

::

    subroutine F1()
      integer profiler(2) / 0, 0 /
      save    profiler

      call TAU_PROFILE_TIMER(profiler,'f1()')
      call TAU_PROFILE_START(profiler)
      ...
      call TAU_PROFILE_STOP(profiler)
    end
      

See Also
========

?, ?

TAU\_PROFILE\_STOP
3
TAU\_PROFILE\_STOP
Stops a timer.
C/C++:
TAU\_PROFILE\_STOP
Profiler
timer
Fortran:
TAU\_PROFILE\_STOP
integer
profiler
(2)
Description
===========

Stops the timer given by ``timer``. It is important to note that timers
can be nested, but not overlapping. TAU detects programming errors that
lead to such overlaps at runtime, and prints a warning message.

Example
=======

**C/C++ :**

::

    int foo(int a) {
      TAU_PROFILE_TIMER(timer, "foo", "int (int)", TAU_USER);
      TAU_PROFILE_START(timer);
      ...
      TAU_PROFILE_STOP(timer);
      return a;
    }
        

**Fortran :**

::

    subroutine F1()
      integer profiler(2) / 0, 0 /
      save    profiler

      call TAU_PROFILE_TIMER(profiler,'f1()')
      call TAU_PROFILE_START(profiler)
      ...
      call TAU_PROFILE_STOP(profiler)
    end
      

See Also
========

?, ?

TAU\_STATIC\_TIMER\_START
3
TAU\_STATIC\_TIMER\_START
Starts a timer.
C/C++:
TAU\_STATIC\_TIMER\_START
Profiler
timer
Fortran:
TAU\_STATIC\_TIMER\_START
integer
profiler
(2)
Description
===========

Starts a static timer defined by ?.

Example
=======

**C/C++ :**

::

    TAU_PROFILE("int foo(int) [{foo.cpp} {13,1}-{20,1}]", " ", TAU_USER);

    printf("inside foo: calling bar: x = %d\n", x);
    printf("before calling bar in foo\n");
    TAU_STATIC_TIMER_START("foo_bar");
    bar(x-1); /* 17 */
    printf("after calling bar in foo\n");
    TAU_STATIC_TIMER_STOP("foo_bar");

**Fortran :**

::

    call TAU_PROFILE_TIMER(profiler, 'FOO [{foo.f90} {8,18}]')
    call TAU_PROFILE_START(profiler)
    print *, "inside foo: calling bar, x = ", x
      call TAU_STATIC_TIMER_START("foo_bar");
        call bar(x-1)
      print *, "after calling bar"
        call TAU_STATIC_TIMER_STOP("foo_bar");
    call TAU_PROFILE_STOP(profiler)  

See Also
========

?, ?, ?

TAU\_STATIC\_TIMER\_STOP
3
TAU\_STATIC\_TIMER\_STOP
Starts a timer.
C/C++:
TAU\_STATIC\_TIMER\_STOP
Profiler
timer
Fortran:
TAU\_STATIC\_TIMER\_STOP
integer
profiler
(2)
Description
===========

Starts a static timer defined by ?.

Example
=======

**C/C++ :**

::

    TAU_PROFILE("int foo(int) [{foo.cpp} {13,1}-{20,1}]", " ", TAU_USER);

    printf("inside foo: calling bar: x = %d\n", x);
    printf("before calling bar in foo\n");
    TAU_STATIC_TIMER_START("foo_bar");
    bar(x-1); /* 17 */
    printf("after calling bar in foo\n");
    TAU_STATIC_TIMER_STOP("foo_bar");

**Fortran :**

::

    call TAU_PROFILE_TIMER(profiler, 'FOO [{foo.f90} {8,18}]')
    call TAU_PROFILE_START(profiler)
    print *, "inside foo: calling bar, x = ", x
      call TAU_STATIC_TIMER_START("foo_bar");
        call bar(x-1)
      print *, "after calling bar"
        call TAU_STATIC_TIMER_STOP("foo_bar");
    call TAU_PROFILE_STOP(profiler)  

See Also
========

?, ?, ?

TAU\_DYNAMIC\_TIMER\_START
3
TAU\_DYNAMIC\_TIMER\_START
Starts a dynamic timer.
C/C++:
TAU\_DYNAMIC\_TIMER\_START
String
name
Fortran:
TAU\_DYNAMIC\_TIMER\_START
integer
iteration
char
name
(size)
Description
===========

Starts a new dynamic timer concating the iterator to the end of the
name.

Example
=======

**C/C++ :**

::

    int foo(int a) {
      TAU_PROFILE_TIMER(timer, "foo", "int (int)", TAU_USER);
      TAU_DYNAMIC_TIMER_START(timer);
      ...
      TAU_PROFILE_STOP(timer);
      return a;
    }
        

**Fortran :**

::

      integer tau_iteration / 0 /
          save tau_iteration
          call TAU_PROFILE_TIMER(profiler, 'FOO1 [{foo.f90} {16,18}]')
          call TAU_PROFILE_START(profiler)
          print *, "inside foo1: calling bar, x = ", x
          tau_iteration = tau_iteration + 1
      call TAU_DYNAMIC_TIMER_START(tau_iteration,"foo1_bar");
            call bar(x-1)
          print *, "after calling bar"
           call TAU_DYNAMIC_TIMER_STOP(tau_iteration,"foo1_bar");
      call TAU_PROFILE_STOP(profiler)
      

See Also
========

?, ?

TAU\_DYNAMIC\_TIMER\_STOP
3
TAU\_DYNAMIC\_TIMER\_STOP
Starts a dynamic timer.
C/C++:
TAU\_DYNAMIC\_TIMER\_STOP
String
name
Fortran:
TAU\_DYNAMIC\_TIMER\_STOP
integer
iteration
char
name
(size)
Description
===========

Stops a new dynamic timer concating the iterator to the end of the
name.\ ``timer``

Example
=======

**C/C++ :**

::

    int foo(int a) {
      TAU_PROFILE_TIMER(timer, "foo", "int (int)", TAU_USER);
      TAU_DYNAMIC_TIMER_START(timer);
      ...
      TAU_PROFILE_STOP(timer);
      return a;
    }
        

**Fortran :**

::

      integer tau_iteration / 0 /
          save tau_iteration
          call TAU_PROFILE_TIMER(profiler, 'FOO1 [{foo.f90} {16,18}]')
          call TAU_PROFILE_START(profiler)
          print *, "inside foo1: calling bar, x = ", x
          tau_iteration = tau_iteration + 1
      call TAU_DYNAMIC_TIMER_START(tau_iteration,"foo1_bar");
            call bar(x-1)
          print *, "after calling bar"
           call TAU_DYNAMIC_TIMER_STOP(tau_iteration,"foo1_bar");
      call TAU_PROFILE_STOP(profiler)
      

See Also
========

?, ?

TAU\_PROFILE\_TIMER\_DYNAMIC
3
TAU\_PROFILE\_TIMER\_DYNAMIC
Defines a dynamic timer.
C/C++:
TAU\_PROFILE\_TIMER\_DYNAMIC
Profiler
timer
char\* or string&
function\_name
char\* or string&
type
TauGroup\_t
group
Fortran:
TAU\_PROFILE\_TIMER\_DYNAMIC
integer
profiler
(2)
character
name
(size)
Description
===========

``TAU_PROFILE_TIMER_DYNAMIC`` operates similar to ``TAU_PROFILE_TIMER``
except that the timer is created each time the statement is invoked.
This way, the name of the timer can be different for each execution.

Example
=======

**C/C++ :**

::

    int main(int argc, char **argv) {
      int i;
      TAU_PROFILE_TIMER(t,"main()", "", TAU_DEFAULT);
      TAU_PROFILE_SET_NODE(0);
      TAU_PROFILE_START(t);

      for (i=0; i&5; i++) {
        char buf[32];
        sprintf(buf, "Iteration %d", i);

        TAU_PROFILE_TIMER_DYNAMIC(timer, buf, "", TAU_USER);
        TAU_PROFILE_START(timer);
        printf("Iteration %d\n", i);
        f1();

        TAU_PROFILE_STOP(timer);
      }
      return 0;
    }
        

**Fortran :**

::

    subroutine ITERATION(val)
      integer val
      character(13) cvar
      integer profiler(2) / 0, 0 /
      save profiler

      print *, "Iteration ", val

      write (cvar,'(a9,i2)') 'Iteration', val
      call TAU_PROFILE_TIMER_DYNAMIC(profiler, cvar)
      call TAU_PROFILE_START(profiler)

      call F1()
      call TAU_PROFILE_STOP(profiler)
      return
    end
      

See Also
========

?, ?, ?

TAU\_PROFILE\_DECLARE\_TIMER
3
TAU\_PROFILE\_DECLARE\_TIMER
Declares a timer for C
C:
TAU\_PROFILE\_DECLARE\_TIMER
Profiler
timer
Description
===========

Because C89 does not allow mixed code and declarations,
``TAU_PROFILE_TIMER`` can only be used once in a function. To declare
two timers in a C function, use ``TAU_PROFILE_DECLARE_TIMER`` and
``TAU_PROFILE_CREATE_TIMER``.

Example
=======

**C :**

::

    int f1(void) {
      TAU_PROFILE_DECLARE_TIMER(t1);
      TAU_PROFILE_DECLARE_TIMER(t2);

      TAU_PROFILE_CREATE_TIMER(t1, "timer1", "", TAU_USER);
      TAU_PROFILE_CREATE_TIMER(t2, "timer2", "", TAU_USER);

      TAU_PROFILE_START(t1);
      ...
      TAU_PROFILE_START(t2);
      ...
      TAU_PROFILE_STOP(t2);
      TAU_PROFILE_STOP(t1);
      return 0;
    }
        

See Also
========

?

TAU\_PROFILE\_CREATE\_TIMER
TAU\_PROFILE\_CREATE\_TIMER
Creates a timer for C
C:
TAU\_PROFILE\_CREATE\_TIMER
Profiler
timer
Description
===========

Because C89 does not allow mixed code and declarations,
``TAU_PROFILE_TIMER`` can only be used once in a function. To declare
two timers in a C function, use ``TAU_PROFILE_DECLARE_TIMER`` and
``TAU_PROFILE_CREATE_TIMER``.

Example
=======

**C :**

::

    int f1(void) {
      TAU_PROFILE_DECLARE_TIMER(t1);
      TAU_PROFILE_DECLARE_TIMER(t2);

      TAU_PROFILE_CREATE_TIMER(t1, "timer1", "", TAU_USER);
      TAU_PROFILE_CREATE_TIMER(t2, "timer2", "", TAU_USER);

      TAU_PROFILE_START(t1);
      ...
      TAU_PROFILE_START(t2);
      ...
      TAU_PROFILE_STOP(t2);
      TAU_PROFILE_STOP(t1);
      return 0;
    }

See Also
========

?, ?, ?

TAU\_GLOBAL\_TIMER
3
TAU\_GLOBAL\_TIMER
Declares a global timer
C/C++:
TAU\_GLOBAL\_TIMER
Profiler
timer
char\* or string&
function\_name
char\* or string&
type
TauGroup\_t
group
Description
===========

As ``TAU_PROFILE_TIMER`` is used within the scope of a block (typically
a routine), ``TAU_GLOBAL_TIMER`` can be used across different routines.

Example
=======

**C/C++ :**

::

    /* f1.c */

    TAU_GLOBAL_TIMER(globalTimer, "global timer", "", TAU_USER);

    /* f2.c */

    TAU_GLOBAL_TIMER_EXTERNAL(globalTimer);
    int foo(void) {
      TAU_GLOBAL_TIMER_START(globalTimer);
      /* ... */
      TAU_GLOBAL_TIMER_STOP();
    }
        

See Also
========

?, ?, ?

TAU\_GLOBAL\_TIMER\_EXTERNAL
TAU\_GLOBAL\_TIMER\_EXTERNAL
Declares a global timer from an external compilation unit
C/C++:
TAU\_GLOBAL\_TIMER\_EXTERNAL
Profiler
timer
Description
===========

``TAU_GLOBAL_TIMER_EXTERNAL`` allows you to access a timer defined in
another compilation unit.

Example
=======

**C/C++ :**

::

    /* f1.c */

    TAU_GLOBAL_TIMER(globalTimer, "global timer", "", TAU_USER);

    /* f2.c */

    TAU_GLOBAL_TIMER_EXTERNAL(globalTimer);
    int foo(void) {
      TAU_GLOBAL_TIMER_START(globalTimer);
      /* ... */
      TAU_GLOBAL_TIMER_STOP();
    }
        

See Also
========

?, ?, ?

TAU\_GLOBAL\_TIMER\_START
3
TAU\_GLOBAL\_TIMER\_START
Starts a global timer
C/C++:
TAU\_GLOBAL\_TIMER\_START
Profiler
timer
Description
===========

``TAU_GLOBAL_TIMER_START`` starts a global timer.

Example
=======

**C/C++ :**

::

    /* f1.c */

    TAU_GLOBAL_TIMER(globalTimer, "global timer", "", TAU_USER);

    /* f2.c */

    TAU_GLOBAL_TIMER_EXTERNAL(globalTimer);
    int foo(void) {
      TAU_GLOBAL_TIMER_START(globalTimer);
      /* ... */
      TAU_GLOBAL_TIMER_STOP();
    }
        

See Also
========

?, ?, ?

TAU\_GLOBAL\_TIMER\_STOP
3
TAU\_GLOBAL\_TIMER\_STOP
Stops a global timer
C/C++:
TAU\_GLOBAL\_TIMER\_STOP
Description
===========

``TAU_GLOBAL_TIMER_STOP`` stops a global timer.

Example
=======

**C/C++ :**

::

    /* f1.c */

    TAU_GLOBAL_TIMER(globalTimer, "global timer", "", TAU_USER);

    /* f2.c */

    TAU_GLOBAL_TIMER_EXTERNAL(globalTimer);
    int foo(void) {
      TAU_GLOBAL_TIMER_START(globalTimer);
      /* ... */
      TAU_GLOBAL_TIMER_STOP();
    }
        

See Also
========

?, ?, ?

TAU\_PHASE
3
TAU\_PHASE
Profile a C++ function as a phase
TAU\_PHASE
char\* or string&
function\_name
char\* or string&
type
TauGroup\_t
group
Description
===========

``TAU_PHASE`` profiles a function as a phase. This macro defines the
function and takes care of the timer start and stop as well. The timer
will stop when the macro goes out of scope (as in C++ destruction).

Example
=======

::

    int foo(char *str) {
      TAU_PHASE(foo","int (char *)",TAU_DEFAULT);
      ...
    }
        

See Also
========

?, ?

TAU\_DYNAMIC\_PHASE
3
TAU\_DYNAMIC\_PHASE
Defines a dynamic phase.
C/C++:
TAU\_DYNAMIC\_PHASE
Phase
phase
char\* or string&
function\_name
char\* or string&
type
TauGroup\_t
group
Fortran:
TAU\_DYNAMIC\_PHASE
integer
phase
(2)
character
name
(size)
Description
===========

``TAU_DYNAMIC_PHASE`` creates a dynamic phase. The name of the timer can
be different for each execution.

Example
=======

**C/C++ :**

::

    int main(int argc, char **argv) {
      int i;
      TAU_PROFILE_TIMER(t,"main()", "", TAU_DEFAULT);
      TAU_PROFILE_SET_NODE(0);
      TAU_PROFILE_START(t);

      for (i=0; i&5; i++) {
        char buf[32];
        sprintf(buf, "Iteration %d", i);

        TAU_DYNAMIC_PHASE(timer, buf, "", TAU_USER);
        TAU_PHASE_START(timer);
        printf("Iteration %d\n", i);
        f1();

        TAU_PHASE_STOP(timer);
      }
      return 0;
    }
        

**Fortran :**

::

    subroutine ITERATION(val)
      integer val
      character(13) cvar
      integer profiler(2) / 0, 0 /
      save profiler

      print *, "Iteration ", val

      write (cvar,'(a9,i2)') 'Iteration', val
      call TAU_DYNAMIC_PHASE(profiler, cvar)
      call TAU_PHASE_START(profiler)

      call F1()
      call TAU_PHASE_STOP(profiler)
      return
    end
      

See Also
========

?, ?, ?

TAU\_PHASE\_CREATE\_DYNAMIC
3
TAU\_PHASE\_CREATE\_DYNAMIC
Defines a dynamic phase.
C/C++:
TAU\_PHASE\_CREATE\_DYNAMIC
Phase
phase
char\* or string&
function\_name
char\* or string&
type
TauGroup\_t
group
Fortran:
TAU\_PHASE\_CREATE\_DYNAMIC
integer
phase
(2)
character
name
(size)
Description
===========

``TAU_PHASE_CREATE_DYNAMIC`` creates a dynamic phase. The name of the
timer can be different for each execution.

Example
=======

**C/C++ :**

::

    int main(int argc, char **argv) {
      int i;
      TAU_PROFILE_TIMER(t,"main()", "", TAU_DEFAULT);
      TAU_PROFILE_SET_NODE(0);
      TAU_PROFILE_START(t);

      for (i=0; i&5; i++) {
        char buf[32];
        sprintf(buf, "Iteration %d", i);

        TAU_PHASE_CREATE_DYNAMIC(timer, buf, "", TAU_USER);
        TAU_PHASE_START(timer);
        printf("Iteration %d\n", i);
        f1();

        TAU_PHASE_STOP(timer);
      }
      return 0;
    }
        

**Fortran :**

::

    subroutine ITERATION(val)
      integer val
      character(13) cvar
      integer profiler(2) / 0, 0 /
      save profiler

      print *, "Iteration ", val

      write (cvar,'(a9,i2)') 'Iteration', val
      call TAU_PHASE_CREATE_DYNAMIC(profiler, cvar)
      call TAU_PHASE_START(profiler)

      call F1()
      call TAU_PHASE_STOP(profiler)
      return
    end
      

See Also
========

?, ?, ?

TAU\_PHASE\_CREATE\_STATIC
3
TAU\_PHASE\_CREATE\_STATIC
Defines a static phase.
C/C++:
TAU\_PHASE\_CREATE\_STATIC
Phase
phase
char\* or string&
function\_name
char\* or string&
type
TauGroup\_t
group
Fortran:
TAU\_PHASE\_CREATE\_STATIC
integer
phase
(2)
character
name
(size)
Description
===========

``TAU_PHASE_CREATE_STATIC`` creates a static phase. Static phases (and
timers) are more efficient than dynamic ones because the function
registration only takes place once.

Example
=======

**C/C++ :**

::

    int f2(void)
    {
      TAU_PHASE_CREATE_STATIC(t2,"IO Phase", "", TAU_USER);
      TAU_PHASE_START(t2);
      input();
      output();
      TAU_PHASE_STOP(t2);
      return 0;
    }

**Fortran :**

::

    subroutine F2()

      integer phase(2) / 0, 0 /
      save    phase

      call TAU_PHASE_CREATE_STATIC(phase,'IO Phase')
      call TAU_PHASE_START(phase)

      call INPUT()
      call OUTPUT()

      call TAU_PHASE_STOP(phase)
    end

>\ **Python:**

::

    import pytau
    ptr = pytau.phase("foo")

    pytau.start(ptr)
    foo(2)
    pytau.stop(ptr) 

See Also
========

?, ?, ?

TAU\_PHASE\_START
3
TAU\_PHASE\_START
Enters a phase.
C/C++:
TAU\_PHASE\_START
Phase
phase
Fortran:
TAU\_PHASE\_START
integer
phase
(2)
Description
===========

``TAU_PHASE_START`` enters a phase. Phases can be nested, but not
overlapped.

Example
=======

**C/C++ :**

::

    int f2(void)
    {
      TAU_PHASE_CREATE_STATIC(t2,"IO Phase", "", TAU_USER);
      TAU_PHASE_START(t2);
      input();
      output();
      TAU_PHASE_STOP(t2);
      return 0;
    }

**Fortran :**

::

    subroutine F2()

      integer phase(2) / 0, 0 /
      save    phase

      call TAU_PHASE_CREATE_STATIC(phase,'IO Phase')
      call TAU_PHASE_START(phase)

      call INPUT()
      call OUTPUT()

      call TAU_PHASE_STOP(phase)
    end

See Also
========

?, ?, ?

TAU\_PHASE\_STOP
3
TAU\_PHASE\_STOP
Exits a phase.
C/C++:
TAU\_PHASE\_STOP
Phase
phase
Fortran:
TAU\_PHASE\_STOP
integer
phase
(2)
Description
===========

``TAU_PHASE_STOP`` exits a phase. Phases can be nested, but not
overlapped.

Example
=======

**C/C++ :**

::

    int f2(void)
    {
      TAU_PHASE_CREATE_STATIC(t2,"IO Phase", "", TAU_USER);
      TAU_PHASE_START(t2);
      input();
      output();
      TAU_PHASE_STOP(t2);
      return 0;
    }

**Fortran :**

::

    subroutine F2()

      integer phase(2) / 0, 0 /
      save    phase

      call TAU_PHASE_CREATE_STATIC(phase,'IO Phase')
      call TAU_PHASE_START(phase)

      call INPUT()
      call OUTPUT()

      call TAU_PHASE_STOP(phase)
    end

See Also
========

?, ?, ?

TAU\_DYNAMIC\_PHASE\_START
3
TAU\_DYNAMIC\_PHASE\_START
Enters a DYNAMIC\_PHASE.
C/C++:
TAU\_DYNAMIC\_PHASE\_START
string
name
Fortran:
TAU\_DYNAMIC\_PHASE\_START
char
name
(size)
Description
===========

``TAU_DYNAMIC_PHASE_START`` enters a DYNAMIC phase. Phases can be
nested, but not overlapped.

Example
=======

**C/C++ :**

::

    TAU_PROFILE("int foo(int) [{foo.cpp} {13,1}-{20,1}]", " ", TAU_USER);

    printf("inside foo: calling bar: x = %d\n", x);
    printf("before calling bar in foo\n");
    TAU_DYNAMIC_PHASE_START("foo_bar");
    bar(x-1); /* 17 */
    printf("after calling bar in foo\n");
    TAU_DYNAMIC_PHASE_STOP("foo_bar");
    return x;
      

**Fortran :**

::

        call TAU_PROFILE_TIMER(profiler, 'FOO [{foo.f90} {8,18}]')
        call TAU_PROFILE_START(profiler)
        print *, "inside foo: calling bar, x = ", x
         call TAU_DYNAMIC_PHASE_START("foo_bar");
          call bar(x-1)
        print *, "after calling bar"
         call TAU_DYNAMIC_PHASE_STOP("foo_bar");
    call TAU_PROFILE_STOP(profiler)
      

See Also
========

?, ?, ?

TAU\_DYNAMIC\_PHASE\_STOP
3
TAU\_DYNAMIC\_PHASE\_STOP
Enters a DYNAMIC\_PHASE.
C/C++:
TAU\_DYNAMIC\_PHASE\_STOP
string
name
Fortran:
TAU\_DYNAMIC\_PHASE\_STOP
char
name
(size)
Description
===========

``TAU_DYNAMIC_PHASE_STOP`` leaves a DYNAMIC phase. Phases can be nested,
but not overlapped.

Example
=======

**C/C++ :**

::

    TAU_PROFILE("int foo(int) [{foo.cpp} {13,1}-{20,1}]", " ", TAU_USER);

    printf("inside foo: calling bar: x = %d\n", x);
    printf("before calling bar in foo\n");
    TAU_DYNAMIC_PHASE_START("foo_bar");
    bar(x-1); /* 17 */
    printf("after calling bar in foo\n");
    TAU_DYNAMIC_PHASE_STOP("foo_bar");
    return x;
      

**Fortran :**

::

        call TAU_PROFILE_TIMER(profiler, 'FOO [{foo.f90} {8,18}]')
        call TAU_PROFILE_START(profiler)
        print *, "inside foo: calling bar, x = ", x
         call TAU_DYNAMIC_PHASE_START("foo_bar");
          call bar(x-1)
        print *, "after calling bar"
         call TAU_DYNAMIC_PHASE_STOP("foo_bar");
    call TAU_PROFILE_STOP(profiler)
      

See Also
========

?, ?, ?

TAU\_STATIC\_PHASE\_START
3
TAU\_STATIC\_PHASE\_START
Enters a STATIC\_PHASE.
C/C++:
TAU\_STATIC\_PHASE\_START
string
name
Fortran:
TAU\_STATIC\_PHASE\_START
char
name
(size)
Description
===========

``TAU_STATIC_PHASE_START`` enters a static phase. Phases can be nested,
but not overlapped.

Example
=======

**C/C++ :**

::

    TAU_PROFILE("int foo(int) [{foo.cpp} {13,1}-{20,1}]", " ", TAU_USER);

    printf("inside foo: calling bar: x = %d\n", x);
    printf("before calling bar in foo\n");
    TAU_STATIC_PHASE_START("foo_bar");
    bar(x-1); /* 17 */
    printf("after calling bar in foo\n");
    TAU_STATIC_PHASE_STOP("foo_bar");
    return x;
      

**Fortran :**

::

        call TAU_PROFILE_TIMER(profiler, 'FOO [{foo.f90} {8,18}]')
        call TAU_PROFILE_START(profiler)
        print *, "inside foo: calling bar, x = ", x
         call TAU_STATIC_PHASE_START("foo_bar");
          call bar(x-1)
        print *, "after calling bar"
         call TAU_STATIC_PHASE_STOP("foo_bar");
    call TAU_PROFILE_STOP(profiler)
      

See Also
========

?, ?, ?

TAU\_STATIC\_PHASE\_STOP
3
TAU\_STATIC\_PHASE\_STOP
Enters a STATIC\_PHASE.
C/C++:
TAU\_STATIC\_PHASE\_STOP
string
name
Fortran:
TAU\_STATIC\_PHASE\_STOP
char
name
(size)
Description
===========

``TAU_STATIC_PHASE_STOP`` leaves a static phase. Phases can be nested,
but not overlapped.

Example
=======

**C/C++ :**

::

    TAU_PROFILE("int foo(int) [{foo.cpp} {13,1}-{20,1}]", " ", TAU_USER);

    printf("inside foo: calling bar: x = %d\n", x);
    printf("before calling bar in foo\n");
    TAU_STATIC_PHASE_START("foo_bar");
    bar(x-1); /* 17 */
    printf("after calling bar in foo\n");
    TAU_STATIC_PHASE_STOP("foo_bar");
    return x;
      

**Fortran :**

::

        call TAU_PROFILE_TIMER(profiler, 'FOO [{foo.f90} {8,18}]')
        call TAU_PROFILE_START(profiler)
        print *, "inside foo: calling bar, x = ", x
         call TAU_STATIC_PHASE_START("foo_bar");
          call bar(x-1)
        print *, "after calling bar"
         call TAU_STATIC_PHASE_STOP("foo_bar");
    call TAU_PROFILE_STOP(profiler)
      

See Also
========

?, ?, ?

TAU\_GLOBAL\_PHASE
3
TAU\_GLOBAL\_PHASE
Declares a global phase
C/C++:
TAU\_GLOBAL\_PHASE
Phase
phase
char\* or string&
function\_name
char\* or string&
type
TauGroup\_t
group
Description
===========

Declares a global phase to be used in multiple compilation units.

Example
=======

**C/C++ :**

::

    /* f1.c */

    TAU_GLOBAL_PHASE(globalPhase, "global phase", "", TAU_USER);

    /* f2.c */

    int bar(void) {
      TAU_GLOBAL_PHASE_START(globalPhase);
      /* ... */
      TAU_GLOBAL_PHASE_STOP(globalPhase);
    }
        

See Also
========

?, ?, ?

TAU\_GLOBAL\_PHASE\_EXTERNAL
3
TAU\_GLOBAL\_PHASE\_EXTERNAL
Declares a global phase from an external compilation unit
C/C++:
TAU\_GLOBAL\_PHASE\_EXTERNAL
Profiler
timer
Description
===========

``TAU_GLOBAL_PHASE_EXTERNAL`` allows you to access a phase defined in
another compilation unit.

Example
=======

**C/C++ :**

::

    /* f1.c */

    TAU_GLOBAL_PHASE(globalPhase, "global phase", "", TAU_USER);

    /* f2.c */

    int bar(void) {
      TAU_GLOBAL_PHASE_START(globalPhase);
      /* ... */
      TAU_GLOBAL_PHASE_STOP(globalPhase);
    }
        

See Also
========

?, ?, ?

TAU\_GLOBAL\_PHASE\_START
3
TAU\_GLOBAL\_PHASE\_START
Starts a global phase
C/C++:
TAU\_GLOBAL\_PHASE\_START
Phase
phase
Description
===========

``TAU_GLOBAL_PHASE_START`` starts a global phase.

Example
=======

**C/C++ :**

::

    /* f1.c */

    TAU_GLOBAL_PHASE(globalPhase, "global phase", "", TAU_USER);

    /* f2.c */

    int bar(void) {
      TAU_GLOBAL_PHASE_START(globalPhase);
      /* ... */
      TAU_GLOBAL_PHASE_STOP(globalPhase);
    }
        

See Also
========

?, ?, ?

TAU\_GLOBAL\_PHASE\_STOP
3
TAU\_GLOBAL\_PHASE\_STOP
Stops a global phase
C/C++:
TAU\_GLOBAL\_PHASE\_STOP
Phase
phase
Description
===========

``TAU_GLOBAL_PHASE_STOP`` stops a global phase.

Example
=======

**C/C++ :**

::

    /* f1.c */

    TAU_GLOBAL_PHASE(globalPhase, "global phase", "", TAU_USER);

    /* f2.c */

    int bar(void) {
      TAU_GLOBAL_PHASE_STOP(globalPhase);
      /* ... */
      TAU_GLOBAL_PHASE_STOP(globalPhase);
    }
        

See Also
========

?, ?, ?

TAU\_PROFILE\_EXIT
3
TAU\_PROFILE\_EXIT
Alerts the profiling system to an exit call
C/C++:
TAU\_PROFILE\_EXIT
const char \*
message
Fortran:
TAU\_PROFILE\_EXIT
character
message
(size)
Description
===========

``TAU_PROFILE_EXIT`` should be called prior to an error exit from the
program so that any profiles or event traces can be dumped to disk
before quitting.

Example
=======

**C/C++ :**

::

    if ((ret = open(...)) < 0) {
      TAU_PROFILE_EXIT("ERROR in opening a file");
      perror("open() failed");
      exit(1);
    }
        

**Fortran :**

::

    call TAU_PROFILE_EXIT('abort called')
        

See Also
========

?

TAU\_REGISTER\_THREAD
3
TAU\_REGISTER\_THREAD
Register a thread with the profiling system
C/C++:
TAU\_REGISTER\_THREAD
Fortran:
TAU\_REGISTER\_THREAD
Description
===========

To register a thread with the profiling system, invoke the
``TAU_REGISTER_THREAD`` macro in the run method of the thread prior to
executing any other TAU macro. This sets up thread identifiers that are
later used by the instrumentation system.

Example
=======

**C/C++ :**

::

    void * threaded_func(void *data) {
      TAU_REGISTER_THREAD();
      { /**** NOTE WE START ANOTHER BLOCK IN THREAD */
        TAU_PROFILE_TIMER(tautimer, "threaded_func()", "int ()", 
                          TAU_DEFAULT);
        TAU_PROFILE_START(tautimer);
        work(); /* work done by this thread */
        TAU_PROFILE_STOP(tautimer);
      }
      return NULL;
    }
        

**Fortran :**

::

    call TAU_REGISTER_THREAD()
        

Caveat
======

PDT based tau\_instrumentor does not insert ``TAU_REGISTER_THREAD``
calls, they must be inserted manually

TAU\_PROFILE\_GET\_NODE
3
TAU\_PROFILE\_GET\_NODE
Returns the measurement system's node id
C/C++:
TAU\_PROFILE\_GET\_NODE
int
node
Fortran:
TAU\_PROFILE\_GET\_NODE
integer
node
Description
===========

``TAU_PROFILE_GET_NODE`` gives the node id for the processes in which it
is called. When using MPI node id is the same as MPI rank.

Example
=======

**C/C++ :**

::

    int main (int argc, char **argv) {
        int nodeid;
      TAU_PROFILE_GET_NODE(nodeid);
      return 0;
    }
        

**Fortran :**

::

         PROGRAM SUM_OF_CUBES
          INTEGER :: N
          call TAU_PROFILE_GET_NODE(N)
          END PROGRAM SUM_OF_CUBES
        

**Python:**

::

    import pytau

    pytau.setNode(0)
            

See Also
========

?

TAU\_PROFILE\_GET\_CONTEXT
3
TAU\_PROFILE\_GET\_CONTEXT
Gives the measurement system's context id
C/C++:
TAU\_PROFILE\_GET\_CONTEXT
int
context
Fortran:
TAU\_PROFILE\_GET\_CONTEXT
integer
context
Description
===========

``TAU_PROFILE_GET_CONTEXT`` gives the context id for the processes in
which it is called.

Example
=======

**C/C++ :**

::

    int main (int argc, char **argv) {
      int i;
      TAU_PROFILE_GET_CONTEXT(i);
      return 0;
    }
        

**Fortran :**

::

         PROGRAM SUM_OF_CUBES
          INTEGER :: C 
            call TAU_PROFILE_GET_CONTEXT(C)
          END PROGRAM SUM_OF_CUBES
        

See Also
========

?

TAU\_PROFILE\_SET\_THREAD
3
TAU\_PROFILE\_SET\_THREAD
Informs the measurement system of the THREAD id
C/C++:
TAU\_PROFILE\_SET\_THREAD
int
THREAD
Fortran:
TAU\_PROFILE\_SET\_THREAD
integer
THREAD
Description
===========

The ``TAU_PROFILE_SET_THREAD`` macro sets the thread identifier of the
executing task for profiling and tracing. Tasks are identified using
node, context and thread ids. The profile data files generated will
accordingly be named profile.<THREAD>.<context>.<thread>. Note that it
is not necessary to call ``TAU_PROFILE_SET_THREAD`` when you configued
with a threading package (including OpenMP).

Example
=======

**C/C++ :**

::

    int main (int argc, char **argv) {
      int ret, i;
      pthread_attr_t  attr;
      pthread_t       tid;
      TAU_PROFILE_TIMER(tautimer,"main()", "int (int, char **)", 
                        TAU_DEFAULT);
      TAU_PROFILE_START(tautimer);
      TAU_PROFILE_INIT(argc, argv);
      TAU_PROFILE_SET_THREAD(0);
      /* ... */
      TAU_PROFILE_STOP(tautimer);
      return 0;
    }
        

**Fortran :**

::

         PROGRAM SUM_OF_CUBES
           integer profiler(2) / 0, 0 /
            save profiler
          INTEGER :: H, T, U
            call TAU_PROFILE_INIT()
            call TAU_PROFILE_TIMER(profiler, 'PROGRAM SUM_OF_CUBES')
            call TAU_PROFILE_START(profiler)
            call TAU_PROFILE_SET_THREAD(0)
          ! This program prints all 3-digit numbers that
          ! equal the sum of the cubes of their digits.
          DO H = 1, 9
            DO T = 0, 9
              DO U = 0, 9
              IF (100*H + 10*T + U == H**3 + T**3 + U**3) THEN
                 PRINT "(3I1)", H, T, U
              ENDIF
              END DO
            END DO
          END DO
          call TAU_PROFILE_STOP(profiler)
          END PROGRAM SUM_OF_CUBES
        

**Python:**

::

    import pytau

    pytau.setThread(0)
            

See Also
========

? ?

TAU\_PROFILE\_GET\_THREAD
3
TAU\_PROFILE\_GET\_THREAD
Gives the measurement system's thread id
C/C++:
TAU\_PROFILE\_GET\_THREAD
int
thread
Fortran:
TAU\_PROFILE\_GET\_THREAD
integer
THREAD
Description
===========

``TAU_PROFILE_GET_THREAD`` gives the thread id for the processes in
which it is called.

Example
=======

**C/C++ :**

::

    int main (int argc, char **argv) {
      int i;
      TAU_PROFILE_GET_THREAD(i);
      return 0;
    }
        

**Fortran :**

::

         PROGRAM SUM_OF_CUBES
          INTEGER :: T
            call TAU_PROFILE_GET_THREAD(T)
          ! This program prints all 3-digit numbers that
          ! equal the sum of the cubes of their digits.
          END PROGRAM SUM_OF_CUBES
        

**Python:**

::

    import pytau
    pytau.getThread(i)
            

See Also
========

? ?

TAU\_PROFILE\_SET\_NODE
3
TAU\_PROFILE\_SET\_NODE
Informs the measurement system of the node id
C/C++:
TAU\_PROFILE\_SET\_NODE
int
node
Fortran:
TAU\_PROFILE\_SET\_NODE
integer
node
Description
===========

The ``TAU_PROFILE_SET_NODE`` macro sets the node identifier of the
executing task for profiling and tracing. Tasks are identified using
node, context and thread ids. The profile data files generated will
accordingly be named profile.<node>.<context>.<thread>. Note that it is
not necessary to call ``TAU_PROFILE_SET_NODE`` when using the TAU MPI
wrapper library.

Example
=======

**C/C++ :**

::

    int main (int argc, char **argv) {
      int ret, i;
      pthread_attr_t  attr;
      pthread_t       tid;
      TAU_PROFILE_TIMER(tautimer,"main()", "int (int, char **)", 
                        TAU_DEFAULT);
      TAU_PROFILE_START(tautimer);
      TAU_PROFILE_INIT(argc, argv);
      TAU_PROFILE_SET_NODE(0);
      /* ... */
      TAU_PROFILE_STOP(tautimer);
      return 0;
    }
        

**Fortran :**

::

         PROGRAM SUM_OF_CUBES
           integer profiler(2) / 0, 0 /
            save profiler
          INTEGER :: H, T, U
            call TAU_PROFILE_INIT()
            call TAU_PROFILE_TIMER(profiler, 'PROGRAM SUM_OF_CUBES')
            call TAU_PROFILE_START(profiler)
            call TAU_PROFILE_SET_NODE(0)
          ! This program prints all 3-digit numbers that
          ! equal the sum of the cubes of their digits.
          DO H = 1, 9
            DO T = 0, 9
              DO U = 0, 9
              IF (100*H + 10*T + U == H**3 + T**3 + U**3) THEN
                 PRINT "(3I1)", H, T, U
              ENDIF
              END DO
            END DO
          END DO
          call TAU_PROFILE_STOP(profiler)
          END PROGRAM SUM_OF_CUBES
        

**Python:**

::

    import pytau

    pytau.setNode(0)
            

See Also
========

?

TAU\_PROFILE\_SET\_CONTEXT
3
TAU\_PROFILE\_SET\_CONTEXT
Informs the measurement system of the context id
C/C++:
TAU\_PROFILE\_SET\_CONTEXT
int
context
Fortran:
TAU\_PROFILE\_SET\_CONTEXT
integer
context
Description
===========

The ``TAU_PROFILE_SET_CONTEXT`` macro sets the context identifier of the
executing task for profiling and tracing. Tasks are identified using
context, context and thread ids. The profile data files generated will
accordingly be named profile.<context>.<context>.<thread>. Note that it
is not necessary to call ``TAU_PROFILE_SET_CONTEXT`` when using the TAU
MPI wrapper library.

Example
=======

**C/C++ :**

::

    int main (int argc, char **argv) {
      int ret, i;
      pthread_attr_t  attr;
      pthread_t       tid;
      TAU_PROFILE_TIMER(tautimer,"main()", "int (int, char **)",
                        TAU_DEFAULT);
      TAU_PROFILE_START(tautimer);
      TAU_PROFILE_INIT(argc, argv);
      TAU_PROFILE_SET_NODE(0);
      TAU_PROFILE_SET_CONTEXT(1);
      /* ... */
      TAU_PROFILE_STOP(tautimer);
      return 0;
    }
        

**Fortran :**

::

         PROGRAM SUM_OF_CUBES
           integer profiler(2) / 0, 0 /
            save profiler
          INTEGER :: H, T, U
            call TAU_PROFILE_INIT()
            call TAU_PROFILE_TIMER(profiler, 'PROGRAM SUM_OF_CUBES')
            call TAU_PROFILE_START(profiler)
            call TAU_PROFILE_SET_NODE(0)
            call TAU_PROFILE_SET_CONTEXT(1)
          ! This program prints all 3-digit numbers that
          ! equal the sum of the cubes of their digits.
          DO H = 1, 9
            DO T = 0, 9
              DO U = 0, 9
              IF (100*H + 10*T + U == H**3 + T**3 + U**3) THEN
                 PRINT "(3I1)", H, T, U
              ENDIF
              END DO
            END DO
          END DO
          call TAU_PROFILE_STOP(profiler)
          END PROGRAM SUM_OF_CUBES
        

See Also
========

?

TAU\_REGISTER\_FORK
3
TAU\_REGISTER\_FORK
Informs the measurement system that a fork has taken place
C/C++:
TAU\_REGISTER\_FORK
int
pid
enum TauFork\_t
option
Description
===========

To register a child process obtained from the fork() syscall, invoke the
``TAU_REGISTER_FORK`` macro. It takes two parameters, the first is the
node id of the child process (typically the process id returned by the
fork call or any 0..N-1 range integer). The second parameter specifies
whether the performance data for the child process should be derived
from the parent at the time of fork ( ``TAU_INCLUDE_PARENT_DATA`` ) or
should be independent of its parent at the time of fork (
``TAU_EXCLUDE_PARENT_DATA`` ). If the process id is used as the node id,
before any analysis is done, all profile files should be converted to
contiguous node numbers (from 0..N-1). It is highly recommended to use
flat contiguous node numbers in this call for profiling and tracing.

Example
=======

**C/C++ :**

::

    pID = fork();
    if (pID == 0) {
      printf("Parent : pid returned %d\n", pID)
    }  else { 
      // If we'd used the TAU_INCLUDE_PARENT_DATA, we get
      // the performance data from the parent in this process
      // as well.
      TAU_REGISTER_FORK(pID, TAU_EXCLUDE_PARENT_DATA);        
      printf("Child : pid = %d", pID);
    }
        

TAU\_REGISTER\_EVENT
3
TAU\_REGISTER\_EVENT
Registers a user event
C/C++:
TAU\_REGISTER\_EVENT
TauUserEvent
variable
char \*
event\_name
Fortran:
TAU\_REGISTER\_EVENT
int
variable
(2)
character
event\_name
(size)
Description
===========

TAU can profile user-defined events using ``TAU_REGISTER_EVENT``. The
meaning of the event is determined by the user. The first argument to
``TAU_REGISTER_EVENT`` is the pointer to an integer array. This array is
declared with a save attribute as shown below.

Example
=======

**C/C++ :**

::

    int user_square(int count) {
      TAU_REGISTER_EVENT(ue1, "UserSquare Event");
      TAU_EVENT(ue1, count * count);
      return 0;
    }
        

**Fortran :**

::

    integer eventid(2)
    save eventid
    call TAU_REGISTER_EVENT(eventid, 'Error in Iteration')
    call TAU_EVENT(eventid, count)
        

See Also
========

?, ?, ?, ?, ?, ?

TAU\_PROFILER\_REGISTER\_EVENT
3
TAU\_PROFILER\_REGISTER\_EVENT
Registers a user event
C/C++:
TAU\_PROFILER\_REGISTER\_EVENT
TauUserEvent
variable
void \*
event
char \*
event\_name
Fortran:
TAU\_PROFILER\_REGISTER\_EVENT
int
integer
(2)
character
event\_name
(size)
Description
===========

TAU can profile user-defined events using
``TAU_PROFILER_REGISTER_EVENT``. The meaning of the event is determined
by the user. The first argument to ``TAU_PROFILER_REGISTER_EVENT`` is
the pointer to an integer array. This array is declared with a save
attribute as shown below.

Example
=======

**C/C++ :**

::

    int user_square(int count) {
      void *ue1;
        TAU_PROFILER_REGISTER_EVENT(ue1, "UserSquare Event");
      TAU_EVENT(ue1, count * count);
      return 0;
    }
        

**Fortran :**

::

    integer eventid(2)
    save eventid
    call TAU_PROFILER_REGISTER_EVENT(eventid, 'Error in Iteration')
    call TAU_EVENT(eventid, count)
        

See Also
========

?, ?, ?, ?, ?, ?

TAU\_EVENT
3
TAU\_TRIGGER\_EVENT
Triggers a user event
C/C++:
TAU\_TRIGGER\_EVENT
const char \*
name
double
value
Fortran:
TAU\_TRIGGER\_EVENT
int
integer
(2)
character
event\_name
(size)
Description
===========

Triggers an named event with the given value

Example
=======

**C/C++ :**

::

    int user_square(int count) {
      TAU_TRIGGER_EVENT("Error in Iteration", count * count);
      return 0;
    }
            

**Fortran :**

::

    call TAU_EVENT(count, 'Error in Iteration')
        

TAU\_EVENT
3
TAU\_TRIGGER\_EVENT\_THREAD
Triggers a user event
C/C++:
TAU\_TRIGGER\_EVENT\_THREAD
const char \*
name
double
value
int
thread
Fortran:
TAU\_TRIGGER\_EVENT\_THREAD
int
integer
(2)
int
integer
(2)
character
event\_name
(size)
Description
===========

Triggers an named event with the given value on a given thead or task.

Example
=======

**C/C++ :**

::

    int user_square(int count) {
      TAU_TRIGGER_EVENT("Error in Iteration", count * count, workTask);
      return 0;
    }
            

**Fortran :**

::

    call TAU_EVENT(count, workTask, 'Error in Iteration')
        

TAU\_EVENT
3
TAU\_EVENT
Triggers a user event
C/C++:
TAU\_EVENT
TauUserEvent
variable
double
value
Fortran:
TAU\_EVENT
integer
variable
(2)
real
value
Description
===========

Triggers an event that was registered with ``TAU_REGISTER_EVENT``.

Example
=======

**C/C++ :**

::

    int user_square(int count) {
      TAU_REGISTER_EVENT(ue1, "UserSquare Event");
      TAU_EVENT(ue1, count * count);
      return 0;
    }
        

**Fortran :**

::

    integer eventid(2)
    save eventid
    call TAU_REGISTER_EVENT(eventid, 'Error in Iteration')
    call TAU_EVENT(eventid, count)
        

See Also
========

?

TAU\_EVENT\_THREAD
3
TAU\_EVENT\_THREAD
Triggers a user event on a given thread
C/C++:
TAU\_EVENT\_THREAD
TauUserEVENT\_THREAD
variable
double
value
int
thread id
Fortran:
TAU\_EVENT\_THREAD
integer
variable
(2)
real
value
integer
thread id
Description
===========

Triggers an event that was registered with ``TAU_REGISTER_EVENT`` on a
given thread.

Example
=======

**C/C++ :**

::

    int user_square(int count) {
      TAU_REGISTER_EVENT(ue1, "UserSquare Event");
      TAU_EVENT_THREAD(ue1, count * count, threadid);
      return 0;
    }
        

**Fortran :**

::

    integer eventid(2)
    save eventid
    call TAU_REGISTER_EVENT(eventid, 'Error in Iteration')
    call TAU_EVENT_THREAD(eventid, count, threadid)
        

See Also
========

?

TAU\_REGISTER\_CONTEXT\_EVENT
3
TAU\_REGISTER\_CONTEXT\_EVENT
Registers a context event
C/C++:
TAU\_REGISTER\_CONTEXT\_EVENT
TauUserEvent
variable
char \*
event\_name
Fortran:
TAU\_REGISTER\_CONTEXT\_EVENT
int
variable
(2)
character
event\_name
(size)
Description
===========

Creates a context event with name. A context event appends the names of
routines executing on the callstack to the name specified by the user.
Whenver a context event is triggered, the callstack is examined to
determine the context of execution. Starting from the parent function
where the event is triggered, TAU walks up the callstack to a depth
specified by the user in the environment variable
``TAU_CALLPATH_DEPTH ``. If this environment variable is not specified,
TAU uses 2 as the default depth. For e.g., if the user registers a
context event with the name "memory used" and specifies 3 as the
callpath depth, and if the event is triggered in two locations (in
routine a, when it was called by b, when it was called by c, and in
routine h, when it was called by g, when it was called by i), then, we'd
see the user defined event information for "memory used: c() => b() =>
a()" and "memory used: i() => g() => h()".

Example
=======

**C/C++ :**

::

    int f2(void)
    {
      static int count = 0;
      count ++;
      TAU_PROFILE("f2()", "(sleeps 2 sec, calls f3)", TAU_USER);
      TAU_REGISTER_CONTEXT_EVENT(event, "Iteration count");
    /*
      if (count == 2)
        TAU_DISABLE_CONTEXT_EVENT(event);
    */
      printf("Inside f2: sleeps 2 sec, calls f3\n");

      TAU_CONTEXT_EVENT(event, 232+count);
      sleep(2);
      f3();
      return 0;
    }
        

**Fortran :**

::

    subroutine foo(id)
      integer id
           
      integer profiler(2) / 0, 0 /
      integer maev(2) / 0, 0 /
      integer mdev(2) / 0, 0 /
      save profiler, maev, mdev

      integer :: ierr
      integer :: h, t, u
      INTEGER, ALLOCATABLE :: STORAGEARY(:)
      DOUBLEPRECISION   edata

      call TAU_PROFILE_TIMER(profiler, 'FOO')
      call TAU_PROFILE_START(profiler)
      call TAU_PROFILE_SET_NODE(0)

      call TAU_REGISTER_CONTEXT_EVENT(maev, "STORAGEARY Alloc [cubes.f:20]")
      call TAU_REGISTER_CONTEXT_EVENT(mdev, "STORAGEARY Dealloc [cubes.f:37]")

      allocate(STORAGEARY(1:999), STAT=IERR)
      edata = SIZE(STORAGEARY)*sizeof(INTEGER)
      call TAU_CONTEXT_EVENT(maev, edata)
      ...
      deallocate(STORAGEARY)
      edata = SIZE(STORAGEARY)*sizeof(INTEGER)
      call TAU_CONTEXT_EVENT(mdev, edata)
      call TAU_PROFILE_STOP(profiler)
      end subroutine foo
         

See Also
========

?, ?, ?, ?, ?, ?, ?, ?

TAU\_CONTEXT\_EVENT
3
TAU\_CONTEXT\_EVENT
Triggers a context event
C/C++:
TAU\_CONTEXT\_EVENT
TauUserEvent
variable
double
value
Fortran:
TAU\_CONTEXT\_EVENT
integer
variable
(2)
real
value
Description
===========

Triggers a context event. A context event associates the name with the
list of routines along the callstack. A context event tracks information
like a user defined event and TAU records the maxima, minima, mean, std.
deviation and the number of samples for each context event. A context
event helps distinguish the data supplied by the user based on the
location where an event occurs and the sequence of actions
(routine/timer invocations) that preceeded the event. The depth of the
the callstack embedded in the context event's name is specified by the
user in the environment variable `` TAU_CALLPATH_DEPTH``. If this
variable is not specified, TAU uses a default depth of 2.

Example
=======

**C/C++ :**

::

    int f2(void)
    {
      static int count = 0;
      count ++;
      TAU_PROFILE("f2()", "(sleeps 2 sec, calls f3)", TAU_USER);
      TAU_REGISTER_CONTEXT_EVENT(event, "Iteration count");
    /*
      if (count == 2)
        TAU_DISABLE_CONTEXT_EVENT(event);
    */
      printf("Inside f2: sleeps 2 sec, calls f3\n");

      TAU_CONTEXT_EVENT(event, 232+count);
      sleep(2);
      f3();
      return 0;
    }
        

**Fortran :**

::

    integer memevent(2) / 0, 0 /
    save memevent
    call TAU_REGISTER_CONTEXT_EVENT(memevent, "STORAGEARY mem allocated')
    call TAU_CONTEXT_EVENT(memevent, SIZEOF(STORAGEARY)*sizeof(INTEGER))
        

See Also
========

?

TAU\_TRIGGER\_CONTEXT\_EVENT
3
TAU\_TRIGGER\_CONTEXT\_EVENT
Triggers a context event
C/C++:
TAU\_TRIGGER\_CONTEXT\_EVENT
const char \*
name
double
value
Fortran:
TAU\_TRIGGER\_CONTEXT\_EVENT
real
value
character
event\_name
(size)
Description
===========

Triggers an event with a name and the list of routines along the
callstack. A context event tracks information like a user defined event
and TAU records the maxima, minima, mean, std. deviation and the number
of samples for each context event. A context event helps distinguish the
data supplied by the user based on the location where an event occurs
and the sequence of actions (routine/timer invocations) that preceeded
the event. The depth of the the callstack embedded in the context
event's name is specified by the user in the environment variable
`` TAU_CALLPATH_DEPTH``. If this variable is not specified, TAU uses a
default depth of 2.

Example
=======

**C/C++ :**

::

    int f2(void)
    {
      static int count = 0;
      count ++;
      TAU_PROFILE("f2()", "(sleeps 2 sec, calls f3)", TAU_USER);
    /*
      if (count == 2)
        TAU_DISABLE_CONTEXT_EVENT(event);
    */
      printf("Inside f2: sleeps 2 sec, calls f3\n");

      TAU_TRIGGER_CONTEXT_EVENT("Iteration count", 232+count);
      sleep(2);
      f3();
      return 0;
    }
        

**Fortran :**

::

    integer memevent(2) / 0, 0 /
    save memevent
    call TAU_TRIGGER_CONTEXT_EVENT(memevent, SIZEOF(STORAGEARY)*sizeof(INTEGER), "STORAGEARY mem allocated")
        

See Also
========

?

TAU\_EVENT
3
TAU\_TRIGGER\_CONTEXT\_EVENT\_THREAD
Triggers a context user event
C/C++:
TAU\_TRIGGER\_CONTEXT\_EVENT\_THREAD
const char \*
name
double
value
int
thread
Fortran:
TAU\_TRIGGER\_CONTEXT\_EVENT\_THREAD
int
integer
(2)
int
integer
(2)
character
event\_name
(size)
Description
===========

Triggers an event with a name and the list of routines along the
callstack. A context event tracks information like a user defined event
and TAU records the maxima, minima, mean, std. deviation and the number
of samples for each context event. A context event helps distinguish the
data supplied by the user based on the location where an event occurs
and the sequence of actions (routine/timer invocations) that preceeded
the event. The depth of the the callstack embedded in the context
event's name is specified by the user in the environment variable
`` TAU_CALLPATH_DEPTH``. If this variable is not specified, TAU uses a
default depth of 2.

Example
=======

**C/C++ :**

::

    int user_square(int count) {
      TAU_TRIGGER_CONTEXT_EVENT_THREAD("Error in Iteration", count * count, workTask);
      return 0;
    }
            

**Fortran :**

::

    call TAU_TRIGGER_CONTEXT_EVENT_THREAD(count, workTask, 'Error in Iteration')
        

TAU\_ENABLE\_CONTEXT\_EVENT
3
TAU\_ENABLE\_CONTEXT\_EVENT
Enable a context event
C/C++:
TAU\_ENABLE\_CONTEXT\_EVENT
TauUserEvent
event
Description
===========

Enables a context event.

Example
=======

**C/C++ :**

::

    int f2(void) {
      static int count = 0;
      count ++;
      TAU_PROFILE("f2()", "(sleeps 2 sec, calls f3)", TAU_USER);
      TAU_REGISTER_CONTEXT_EVENT(event, "Iteration count");

      if (count == 2)
        TAU_DISABLE_CONTEXT_EVENT(event);
      else
        TAU_ENABLE_CONTEXT_EVENT(event);

      printf("Inside f2: sleeps 2 sec, calls f3\n");

      TAU_CONTEXT_EVENT(event, 232+count);
      sleep(2);
      f3();
      return 0;
    }
        

See Also
========

?, ?

TAU\_DISABLE\_CONTEXT\_EVENT
3
TAU\_DISABLE\_CONTEXT\_EVENT
Disable a context event
C/C++:
TAU\_DISABLE\_CONTEXT\_EVENT
TauUserEvent
event
Description
===========

Disables a context event.

Example
=======

**C/C++ :**

::

    int f2(void) {
      static int count = 0;
      count ++;
      TAU_PROFILE("f2()", "(sleeps 2 sec, calls f3)", TAU_USER);
      TAU_REGISTER_CONTEXT_EVENT(event, "Iteration count");

      if (count == 2)
        TAU_DISABLE_CONTEXT_EVENT(event);
      else
        TAU_ENABLE_CONTEXT_EVENT(event);

      printf("Inside f2: sleeps 2 sec, calls f3\n");

      TAU_CONTEXT_EVENT(event, 232+count);
      sleep(2);
      f3();
      return 0;
    }
        

See Also
========

?, ?

TAU\_EVENT\_SET\_NAME
3
TAU\_EVENT\_SET\_NAME
Sets the name of an event
C/C++:
TAU\_EVENT\_SET\_NAME
TauUserEvent
event
const char \*
name
Description
===========

Changes the name of an event.

Example
=======

**C/C++ :**

::

    TAU_EVENT_SET_NAME(event, "new name");
        

See Also
========

?

TAU\_EVENT\_DISABLE\_MAX
3
TAU\_EVENT\_DISABLE\_MAX
Disables tracking of maximum statistic for a given event
C/C++:
TAU\_EVENT\_DISABLE\_MAX
TauUserEvent
event
Description
===========

Disables tracking of maximum statistic for a given event

Example
=======

**C/C++ :**

::

    TAU_EVENT_DISABLE_MAX(event);
        

See Also
========

?

TAU\_EVENT\_DISABLE\_MEAN
3
TAU\_EVENT\_DISABLE\_MEAN
Disables tracking of mean statistic for a given event
C/C++:
TAU\_EVENT\_DISABLE\_MEAN
TauUserEvent
event
Description
===========

Disables tracking of mean statistic for a given event

Example
=======

**C/C++ :**

::

    TAU_EVENT_DISABLE_MEAN(event);
        

See Also
========

?

TAU\_EVENT\_DISABLE\_MIN
3
TAU\_EVENT\_DISABLE\_MIN
Disables tracking of minimum statistic for a given event
C/C++:
TAU\_EVENT\_DISABLE\_MIN
TauUserEvent
event
Description
===========

Disables tracking of minimum statistic for a given event

Example
=======

**C/C++ :**

::

    TAU_EVENT_DISABLE_MIN(event);
        

See Also
========

?

TAU\_EVENT\_DISABLE\_STDDEV
3
TAU\_EVENT\_DISABLE\_STDDEV
Disables tracking of standard deviation statistic for a given event
C/C++:
TAU\_EVENT\_DISABLE\_STDDEV
TauUserEvent
event
Description
===========

Disables tracking of standard deviation statistic for a given event

Example
=======

**C/C++ :**

::

    TAU_EVENT_DISABLE_STDDEV(event);
        

See Also
========

?

TAU\_REPORT\_STATISTICS
3
TAU\_REPORT\_STATISTICS
Outputs statistics
C/C++:
TAU\_REPORT\_STATISTICS
Fortran:
TAU\_REPORT\_STATISTICS
Description
===========

``TAU_REPORT_STATISTICS`` prints the aggregate statistics of user events
across all threads in each node. Typically, this should be called just
before the main thread exits.

Example
=======

**C/C++ :**

::

    TAU_REPORT_STATISTICS();
        

**Fortran :**

::

    call TAU_REPORT_STATISTICS()
        

See Also
========

?, ?, ?

TAU\_REPORT\_THREAD\_STATISTICS
3
TAU\_REPORT\_THREAD\_STATISTICS
Outputs statistics, plus thread statistics
C/C++:
TAU\_REPORT\_THREAD\_STATISTICS
Fortran:
TAU\_REPORT\_THREAD\_STATISTICS
Description
===========

``TAU_REPORT_THREAD_STATISTICS`` prints the aggregate, as well as per
thread user event statistics. Typically, this should be called just
before the main thread exits.

Example
=======

**C/C++ :**

::

    TAU_REPORT_THREAD_STATISTICS();
        

**Fortran :**

::

    call TAU_REPORT_THREAD_STATISTICS()
        

See Also
========

?, ?, ?

TAU\_ENABLE\_INSTRUMENTATION
3
TAU\_ENABLE\_INSTRUMENTATION
Enables instrumentation
C/C++:
TAU\_ENABLE\_INSTRUMENTATION
Fortran:
TAU\_ENABLE\_INSTRUMENTATION
Description
===========

``TAU_ENABLE_INSTRUMENTATION`` macro re-enables all TAU instrumentation.
All instances of functions and statements that occur between the
disable/enable section are ignored by TAU. This allows a user to limit
the trace size, if the macros are used to disable recording of a set of
iterations that have the same characteristics as, for example, the first
recorded instance.

Example
=======

**C/C++ :**

::

    int main(int argc, char **argv) { 
      foo();
      TAU_DISABLE_INSTRUMENTATION();
      for (int i =0; i < N; i++) { 
        bar();  // not recorded
      }
      TAU_ENABLE_INSTRUMENTATION();
      bar(); // recorded
    } 
        

**Fortran :**

::

    call TAU_DISABLE_INSTRUMENTATION()
    ...
    call TAU_ENABLE_INSTRUMENTATION()
        

**Python:**

::

    import pytau

    pytau.enableInstrumentation()
    ...
    pytau.disableInstrumentation()
            

See Also
========

?, ?, ?, ?, ?

TAU\_DISABLE\_INSTRUMENTATION
3
TAU\_DISABLE\_INSTRUMENTATION
Disables instrumentation
C/C++:
TAU\_DISABLE\_INSTRUMENTATION
Fortran:
TAU\_DISABLE\_INSTRUMENTATION
Description
===========

``TAU_DISABLE_INSTRUMENTATION`` macro disables all entry/exit
instrumentation within all threads of a context. This allows the user to
selectively enable and disable instrumentation in parts of his/her code.
It is important to re-enable the instrumentation within the same basic
block and scope.

Example
=======

**C/C++ :**

::

    int main(int argc, char **argv) { 
      foo();
      TAU_DISABLE_INSTRUMENTATION();
      for (int i =0; i < N; i++) { 
        bar();  // not recorded
      }
      TAU_DISABLE_INSTRUMENTATION();
      bar(); // recorded
    } 
        

**Fortran :**

::

    call TAU_DISABLE_INSTRUMENTATION()
    ...
    call TAU_DISABLE_INSTRUMENTATION()
        

**Python:**

::

    import pytau

    pytau.enableInstrumentation()
    ...
    pytau.disableInstrumentation()
            

See Also
========

?, ?, ?, ?, ?

TAU\_ENABLE\_GROUP
3
TAU\_ENABLE\_GROUP
Enables tracking of a given group
C/C++:
TAU\_ENABLE\_GROUP
TauGroup\_t
group
Fortran:
TAU\_ENABLE\_GROUP
integer
group
Description
===========

Enables the instrumentation for a given group. By default, it is already
on.

Example
=======

**C/C++ :**

::

    void foo() {
      TAU_PROFILE("foo()", " ", TAU_USER);
      ...
      TAU_ENABLE_GROUP(TAU_USER);
    }
        

**Fortran :**

::

      include 'Profile/TauFAPI.h'
      call TAU_ENABLE_GROUP(TAU_USER)
        

**Python:**

::

    import pytau

    pytau.enableGroup(TAU_USER)
            

See Also
========

?, ?, ?, ?, ?

TAU\_DISABLE\_GROUP
3
TAU\_DISABLE\_GROUP
Disables tracking of a given group
C/C++:
TAU\_DISABLE\_GROUP
TauGroup\_t
group
Fortran:
TAU\_DISABLE\_GROUP
integer
group
Description
===========

Disables the instrumentation for a given group. By default, it is on.

Example
=======

**C/C++ :**

::

    void foo() {
      TAU_PROFILE("foo()", " ", TAU_USER);
      ...
      TAU_DISABLE_GROUP(TAU_USER);
    }
        

**Fortran :**

::

      include 'Profile/TauFAPI.h'
      call TAU_DISABLE_GROUP(TAU_USER)
        

**Python:**

::

    import pytau

    pytau.disableGroup(TAU_USER)
            

See Also
========

?, ?, ?, ?, ?

TAU\_PROFILE\_TIMER\_SET\_GROUP
3
TAU\_PROFILE\_TIMER\_SET\_GROUP
Change the group of a timer
C/C++:
TAU\_PROFILE\_TIMER\_SET\_GROUP
Profiler
timer
TauGroup\_t
group
Description
===========

``TAU_PROFILE_TIMER_SET_GROUP`` changes the group associated with a
timer.

Example
=======

**C/C++ :**

::

    void foo() {
      TAU_PROFILE_TIMER(t, "foo loop timer", " ", TAU_USER1);
      ...
      TAU_PROFILE_TIMER_SET_GROUP(t, TAU_USER3);
    }
        

See Also
========

?, ?

TAU\_PROFILE\_TIMER\_SET\_GROUP\_NAME
3
TAU\_PROFILE\_TIMER\_SET\_GROUP\_NAME
Changes the group name for a timer
C/C++:
TAU\_PROFILE\_TIMER\_SET\_GROUP\_NAME
Profiler
timer
char \*
groupname
Description
===========

``TAU_PROFILE_TIMER_SET_GROUP_NAME`` changes the group name associated
with a given timer.

Example
=======

**C/C++ :**

::

    void foo() {
      TAU_PROFILE_TIMER(looptimer, "foo: loop1", " ", TAU_USER);
      TAU_PROFILE_START(looptimer);
      for (int i = 0; i < N; i++) { /* do something */ }
      TAU_PROFILE_STOP(looptimer);
      TAU_PROFILE_TIMER_SET_GROUP_NAME("Field");
    }
        

See Also
========

?, ?

TAU\_PROFILE\_TIMER\_SET\_NAME
3
TAU\_PROFILE\_TIMER\_SET\_NAME
Changes the name of a timer
C/C++:
TAU\_PROFILE\_TIMER\_SET\_NAME
Profiler
timer
string
newname
Description
===========

``TAU_PROFILE_TIMER_SET_NAME`` macro changes the name associated with a
timer to the newname argument.

Example
=======

**C/C++ :**

::

    void foo() {
      TAU_PROFILE_TIMER(timer1, "foo:loop1", " ", TAU_USER);
      ...
      TAU_PROFILE_TIMER_SET_NAME(timer1, "foo:lines 21-34");
    }
        

See Also
========

?

TAU\_PROFILE\_TIMER\_SET\_TYPE
3
TAU\_PROFILE\_TIMER\_SET\_TYPE
Changes the type of a timer
C/C++:
TAU\_PROFILE\_TIMER\_SET\_TYPE
Profiler
timer
string
newname
Description
===========

``TAU_PROFILE_TIMER_SET_TYPE`` macro changes the type associated with a
timer to the newname argument.

Example
=======

**C/C++ :**

::

    void foo() {
      TAU_PROFILE_TIMER(timer1, "foo", "int", TAU_USER);
      ...
      TAU_PROFILE_TIMER_SET_TYPE(timer1, "long");
    }
        

See Also
========

?

TAU\_PROFILE\_SET\_GROUP\_NAME
3
TAU\_PROFILE\_SET\_GROUP\_NAME
Changes the group name of a profiled section
C/C++:
TAU\_PROFILE\_SET\_GROUP\_NAME
char \*
groupname
Description
===========

``TAU_PROFILE_SET_GROUP_NAME`` macro allows the user to change the group
name associated with the instrumented routine. This macro must be called
within the instrumented routine.

Example
=======

**C/C++ :**

::

    void foo() {
      TAU_PROFILE("foo()", "void ()", TAU_USER);
      TAU_PROFILE_SET_GROUP_NAME("Particle"); 
      /* gives a more meaningful group name */
    }
        

See Also
========

?

TAU\_INIT
3
TAU\_INIT
Processes command-line arguments for selective instrumentation
C/C++:
TAU\_INIT
int \*
argc
char \*\*\*
argv
Description
===========

``TAU_INIT`` parses and removes the command-line arguments for the names
of profile groups that are to be selectively enabled for
instrumentation. By default, if this macro is not used, functions
belonging to all profile groups are enabled. ``TAU_INIT`` differs from
``TAU_PROFILE_INIT`` only in the argument types.

Example
=======

**C/C++ :**

::

    int main(int argc, char **argv) {
      TAU_PROFILE("main()", "int (int, char **)", TAU_GROUP_12);
      TAU_INIT(&argc, &argv);
      ...
    }

    % ./a.out --profile 12+14
        

See Also
========

?

TAU\_PROFILE\_INIT
3
TAU\_PROFILE\_INIT
Processes command-line arguments for selective instrumentation
C/C++:
TAU\_PROFILE\_INIT
int
argc
char \*\*
argv
Fortran:
TAU\_PROFILE\_INIT
Description
===========

``TAU_PROFILE_INIT`` parses the command-line arguments for the names of
profile groups that are to be selectively enabled for instrumentation.
By default, if this macro is not used, functions belonging to all
profile groups are enabled. ``TAU_INIT`` differs from
``TAU_PROFILE_INIT`` only in the argument types.

Example
=======

**C/C++ :**

::

    int main(int argc, char **argv) {
      TAU_PROFILE("main()", "int (int, char **)", TAU_DEFAULT);
      TAU_PROFILE_INIT(argc, argv);
      ...
    }

    % ./a.out --profile 12+14
        

**Fortran :**

::

    PROGRAM SUM_OF_CUBES
      integer profiler(2)
      save profiler
          
      call TAU_PROFILE_INIT()
      ...
        

See Also
========

?

TAU\_GET\_PROFILE\_GROUP
3
TAU\_GET\_PROFILE\_GROUP
Creates groups based on names
C/C++:
TAU\_GET\_PROFILE\_GROUP
char \*
groupname
Description
===========

``TAU_GET_PROFILE_GROUP`` allows the user to dynamically create groups
based on strings, rather than use predefined, statically assigned groups
such as ``TAU_USER1, TAU_USER2`` etc. This allows names to be associated
in creating unique groups that are more meaningful, using names of files
or directories for instance.

Example
=======

**C/C++ :**

::

    #define PARTICLES TAU_GET_PROFILE_GROUP("PARTICLES")

    void foo() {
      TAU_PROFILE("foo()", " ", PARTICLES);
    }

    void bar() {
      TAU_PROFILE("bar()", " ", PARTICLES);
    }
        

**Python:**

::

    import pytau

    pytau.getProfileGroup("PARTICLES")
            

See Also
========

?, ?, ?, ?

TAU\_ENABLE\_GROUP\_NAME
3
TAU\_ENABLE\_GROUP\_NAME
Enables a group based on name
C/C++:
TAU\_ENABLE\_GROUP\_NAME
char \*
groupname
Fortran:
TAU\_ENABLE\_GROUP\_NAME
character
groupname
(size)
Description
===========

``TAU_ENABLE_GROUP_NAME`` macro can turn on the instrumentation
associated with routines based on a dynamic group assigned to them. It
is important to note that this and the ``TAU_DISABLE_GROUP_NAME`` macros
apply to groups created dynamically using ``TAU_GET_PROFILE_GROUP.``

Example
=======

**C/C++ :**

::

    /* tau_instrumentor was invoked with -g DTM for a set of files */
    TAU_DISABLE_GROUP_NAME("DTM"); 
    dtm_routines();
    /* disable and then re-enable the group with the name DTM */
    TAU_ENABLE_GROUP_NAME("DTM");
        

**Fortran :**

::

    ! tau_instrumentor was invoked with -g DTM for this file 
        call TAU_PROFILE_TIMER(profiler, "ITERATE>DTM")

        call TAU_DISABLE_GROUP_NAME("DTM")
    ! Disable, then re-enable DTM group
        call TAU_ENABLE_GROUP_NAME("DTM")
        

**Python:**

::

    import pytau

    pytau.enableGroupName("DTM")
            

See Also
========

?, ?, ?, ?

TAU\_DISABLE\_GROUP\_NAME
3
TAU\_DISABLE\_GROUP\_NAME
Disables a group based on name
C/C++:
TAU\_DISABLE\_GROUP\_NAME
char \*
groupname
Fortran:
TAU\_DISABLE\_GROUP\_NAME
character
groupname
(size)
Description
===========

Similar to ``TAU_ENABLE_GROUP_NAME`` , this macro turns off the
instrumentation in all routines associated with the dynamic group
created using the tau\_instrumentor -g <group\_name> argument.

Example
=======

**C/C++ :**

::

    /* tau_instrumentor was invoked with -g DTM for a set of files */
    TAU_DISABLE_GROUP_NAME("DTM"); 
    dtm_routines();
    /* disable and then re-enable the group with the name DTM */
    TAU_ENABLE_GROUP_NAME("DTM");
        

**Fortran :**

::

    ! tau_instrumentor was invoked with -g DTM for this file 
        call TAU_PROFILE_TIMER(profiler, "ITERATE>DTM")

        call TAU_DISABLE_GROUP_NAME("DTM")
    ! Disable, then re-enable DTM group
        call TAU_ENABLE_GROUP_NAME("DTM")
        

**Python:**

::

    import pytau

    pytau.disableGroupName("DTM")
            

See Also
========

?, ?, ?, ?

TAU\_ENABLE\_ALL\_GROUPS
3
TAU\_ENABLE\_ALL\_GROUPS
Enables instrumentation in all groups
C/C++:
TAU\_ENABLE\_ALL\_GROUPS
Fortran:
TAU\_ENABLE\_ALL\_GROUPS
Description
===========

This macro turns on instrumentation in all groups

Example
=======

**C/C++ :**

::

    TAU_ENABLE_ALL_GROUPS();      
        

**Fortran :**

::

    call TAU_ENABLE_ALL_GROUPS();
        

**Python:**

::

    import pytau

    pytau.enableAllGroups()
         

See Also
========

?, ?, ?, ?

TAU\_DISABLE\_ALL\_GROUPS
3
TAU\_DISABLE\_ALL\_GROUPS
Disables instrumentation in all groups
C/C++:
TAU\_DISABLE\_ALL\_GROUPS
Fortran:
TAU\_DISABLE\_ALL\_GROUPS
Description
===========

This macro turns off instrumentation in all groups.

Example
=======

**C/C++ :**

::

    void foo() {
      TAU_DISABLE_ALL_GROUPS();
      TAU_ENABLE_GROUP_NAME("PARTICLES");
    }
        

**Fortran :**

::

    call TAU_DISABLE_ALL_GROUPS();
        

**Python:**

::

    import pytau

    pytau.disableAllGroups()
            

See Also
========

?, ?, ?, ?

TAU\_GET\_EVENT\_NAMES
3
TAU\_GET\_EVENT\_NAMES
Gets the registered user events.
C/C++:
TAU\_GET\_EVENT\_NAMES
const char \*\*\*
eventList
int \*
numEvents
Description
===========

Retrieves user event names for all user-defined events

Example
=======

**C/C++ :**

::

    const char **eventList;
    int numEvents;

    TAU_GET_EVENT_NAMES(eventList, numEvents);

    cout << "numEvents: " << numEvents << endl;

        

See Also
========

?, ?, ?

TAU\_GET\_EVENT\_VALS
3
TAU\_GET\_EVENT\_VALS
Gets user event data for given user events.
C/C++:
TAU\_GET\_EVENT\_VALS
const char \*\*
inUserEvents
int
numUserEvents
int \*\*
numEvents
double \*\*
max
double \*\*
min
double \*\*
mean
double \*\*
sumSqe
Description
===========

Retrieves user defined event data for the specified user defined events.
The list of events are specified by the first parameter (eventList) and
the user specifies the number of events in the second parameter
(numUserEvents). TAU returns the number of times the event was invoked
in the numUserEvents. The max, min, mean values are returned in the
following parameters. TAU computes the sum of squares of the given event
and returns this value in the next argument (sumSqe).

Example
=======

**C/C++ :**

::

      const char **eventList;
      int numEvents;

      TAU_GET_EVENT_NAMES(eventList, numEvents);

      cout << "numEvents: " << numEvents << endl;

      if (numEvents > 0) {
        int *numSamples;
        double *max;
        double *min;
        double *mean;
        double *sumSqr;

        TAU_GET_EVENT_VALS(eventList, numEvents, numSamples, 
          max, min, mean, sumSqr);
        for (int i=0; i<numEvents; i++) {
          cout << "-------------------\n";
          cout << "User Event:        " << eventList[i] << endl;
          cout << "Number of Samples: " << numSamples[i] << endl;
          cout << "Maximum Value:     " << max[i] << endl;
          cout << "Minimum Value:     " << min[i] << endl;
          cout << "Mean Value:        " << mean[i] << endl;
          cout << "Sum Squared:       " << sumSqr[i] << endl;
        }
      }
    }

        

See Also
========

?, ?, ?

TAU\_GET\_COUNTER\_NAMES
3
TAU\_GET\_COUNTER\_NAMES
Gets the counter names
C/C++:
TAU\_GET\_COUNTER\_NAMES
char \*\*
counterList
int
numCounters
Description
===========

``TAU_GET_COUNTER_NAMES`` returns the list of counter names and the
number of counters used for measurement. When wallclock time is used,
the counter name of "default" is returned.

Example
=======

**C/C++ :**

::

    int numOfCounters;
    const char ** counterList;

    TAU_GET_COUNTER_NAMES(counterList, numOfCounters);

    for(int j=0;j<numOfCounters;j++){ 
      cout << "The counter names so far are: " << counterList[j] << endl;
    }
        

**Python:**

::

    import pytau

    pytau.getCounterNames(counterList, numOfCounters);
            

See Also
========

?, ?

TAU\_GET\_FUNC\_NAMES
3
TAU\_GET\_FUNC\_NAMES
Gets the function names
C/C++:
TAU\_GET\_FUNC\_NAMES
char \*\*
functionList
int
numFuncs
Description
===========

This macro fills the funcList argument with the list of timer and
routine names. It also records the number of routines active in the
numFuncs argument.

Example
=======

**C/C++ :**

::

      const char ** functionList;
      int numOfFunctions;

      TAU_GET_FUNC_NAMES(functionList, numOfFunctions);

      for(int i=0;i<numOfFunctions;i++){
        cout << "This function names so far are: " << functionList[i] << endl;
      }

        

*Python:*

::

    import pytau

    pytau.getFuncNames(functionList, numOfFunctions)
            

See Also
========

?, ?, ?, ?

TAU\_GET\_FUNC\_VALS
3
TAU\_GET\_FUNC\_VALS
Gets detailed performance data for given functions
C/C++:
TAU\_GET\_FUNC\_VALS
const char \*\*
inFuncs
int
numOfFuncs
double \*\*\*
counterExclusiveValues
double \*\*\*
counterInclusiveValues
int \*\*
numOfCalls
int \*\*
numOfSubRoutines
const char \*\*\*
counterNames
int \*
numOfCounters
int
tid
Description
===========

It gets detailed performance data for the list of routines. The user
specifies inFuncs and the number of routines; TAU then returns the other
arguments with the performance data. counterExclusiveValues and
counterInclusiveValues are two dimensional arrays: the first dimension
is the routine id and the second is counter id. The value is indexed by
these two dimensions. numCalls and numSubrs (or child routines) are one
dimensional arrays.

Example
=======

**C/C++ :**

::

    const char **inFuncs;
    /* The first dimension is functions, and the 
    second dimension is counters */
    double **counterExclusiveValues;
    double **counterInclusiveValues;
    int *numOfCalls;
    int *numOfSubRoutines;
    const char **counterNames;
    int numOfCouns;
          
    TAU_GET_FUNC_NAMES(functionList, numOfFunctions);
          
    /* We are only interested in the first two routines 
    that are executing in this context. So, we allocate 
    space for two routine names and get the performance 
    data for these two routines at runtime. */
    if (numOfFunctions >=2 ) {
      inFuncs = (const char **) malloc(sizeof(const char *) * 2);
          
      inFuncs[0] = functionList[0];
      inFuncs[1] = functionList[1];
          
      //Just to show consistency.
      TAU_DB_DUMP();
          
      TAU_GET_FUNC_VALS(inFuncs, 2,
      counterExclusiveValues,
      counterInclusiveValues,
      numOfCalls,
      numOfSubRoutines,
      counterNames,
      numOfCouns);
          
      TAU_DUMP_FUNC_VALS_INCR(inFuncs, 2);
          
          
      cout << "@@@@@@@@@@@@@@@" << endl;
      cout << "The number of counters is: " << numOfCouns << endl;
      cout << "The first counter is: " << counterNames[0] << endl;
          
      cout << "The Exclusive value of: " << inFuncs[0]
      << " is: " << counterExclusiveValues[0][0] << endl;
      cout << "The numOfSubRoutines of: " << inFuncs[0]
      << " is: " << numOfSubRoutines[0]
      << endl;
          
          
      cout << "The Inclusive value of: " << inFuncs[1]
      << " is: " << counterInclusiveValues[1][0]
      << endl;
      cout << "The numOfCalls of: " << inFuncs[1]
      << " is: " << numOfCalls[1]
      << endl;

      cout << "@@@@@@@@@@@@@@@" << endl;
    }
          
    TAU_DB_DUMP_INCR();
        

Python:

::

    import pytau

    pytau.dumpFuncVals("foo", "bar", "bar2")
            

See Also
========

?, ?, ?, ?

TAU\_ENABLE\_TRACKING\_MEMORY
3
TAU\_ENABLE\_TRACKING\_MEMORY
Enables memory tracking
C/C++:
TAU\_ENABLE\_TRACKING\_MEMORY
Fortran:
TAU\_ENABLE\_TRACKING\_MEMORY
Description
===========

Enables tracking of the heap memory utilization in the program. TAU
takes a sample of the heap memory utilized (as reported by the mallinfo
system call) and associates it with a single global user defined event.
An interrupt is generated every 10 seconds and the value of the heap
memory used is recorded in the user defined event. The inter-interrupt
interval (default of 10 seconds) may be set by the user using the call
``TAU_SET_INTERRUPT_INTERVAL``.

Example
=======

**C/C++ :**

::

    TAU_ENABLE_TRACKING_MEMORY();      
        

**Fortran :**

::

    call TAU_ENABLE_TRACKING_MEMORY()
        

**Python:**

::

    import pytau

    pytau.enableTrackingMemory()
            

See Also
========

?, ?, ?, ?

TAU\_DISABLE\_TRACKING\_MEMORY
3
TAU\_DISABLE\_TRACKING\_MEMORY
Disables memory tracking
C/C++:
TAU\_DISABLE\_TRACKING\_MEMORY
Fortran:
TAU\_DISABLE\_TRACKING\_MEMORY
Description
===========

Disables tracking of heap memory utilization. This call may be used in
sections of code where TAU should not interrupt the execution to
periodically track the heap memory utilization.

Example
=======

**C/C++ :**

::

    TAU_DISABLE_TRACKING_MEMORY();      
        

**Fortran :**

::

    call TAU_DISABLE_TRACKING_MEMORY()
        

**Python:**

::

    import pytau

    pytau.disableTrackingMemory()

            

See Also
========

?, ?, ?, ?

TAU\_TRACK\_POWER
3
TAU\_TRACK\_POWER
Initializes POWER tracking system
C/C++:
TAU\_TRACK\_POWER
Fortran:
TAU\_TRACK\_POWER
Description
===========

For power profiling, there are two modes of operation: 1) the user
explicitly inserts TAU\_TRACK\_POWER\_HERE() calls in the source code
and the power event is triggered at those locations, and 2) the user
enables tracking POWER by calling TAU\_TRACK\_POWER() and an interrupt
is generated every 10 seconds and the POWER event is triggered with the
current value. Also, this interrupt interval can be changed by calling
TAU\_SET\_INTERRUPT\_INTERVAL(value). The tracking of power events in
both cases can be explictly enabled or disabled by calling the macros
TAU\_ENABLE\_TRACKING\_POWER() or TAU\_DISABLE\_TRACKING\_()
respectively.

Example
=======

**C/C++ :**

::

    TAU_TRACK_POWER();      
        

**Fortran :**

::

    call TAU_TRACK_POWER()
        

**Python:**

::

    import pytau

    pytau.trackPower()
        

See Also
========

?, ?, ?, ?, ?

TAU\_TRACK\_POWER\_HERE
3
TAU\_TRACK\_POWER\_HERE
Triggers power tracking at a given execution point
C/C++:
TAU\_TRACK\_POWER\_HERE
Fortran:
TAU\_TRACK\_POWER\_HERE
Description
===========

Triggers power tracking at a given execution point

Example
=======

**C/C++ :**

::

    int main(int argc, char **argv) {
      TAU_PROFILE("main()", " ", TAU_DEFAULT);
      TAU_PROFILE_SET_NODE(0);

      TAU_TRACK_POWER_HERE();

      int *x = new int[5*1024*1024];
      TAU_TRACK_POWER_HERE();
      return 0;
    }
        

**Fortran :**

::

    INTEGER, ALLOCATABLE :: STORAGEARY(:)
    allocate(STORAGEARY(1:999), STAT=IERR)

    ! if we wish to record a sample of the heap POWER 
    ! utilization at this point, invoke the following call:
    call TAU_TRACK_POWER_HERE()

        

**Python:**

::

    import pytau

    pytau.trackPowerHere()
            

See Also
========

?

TAU\_ENABLE\_TRACKING\_POWER
3
TAU\_ENABLE\_TRACKING\_POWER
Enables power headroom tracking
C/C++:
TAU\_ENABLE\_TRACKING\_POWER
Fortran:
TAU\_ENABLE\_TRACKING\_POWER
Description
===========

``TAU_ENABLE_TRACKING_POWER()`` enables power tracking after a
``TAU_DISABLE_TRACKING_POWER()``.

Example
=======

**C/C++ :**

::

    TAU_DISABLE_TRACKING_POWER();
    /* do some work */
    ...
    /* re-enable tracking POWER */
    TAU_ENABLE_TRACKING_POWER();
        

**Fortran :**

::

    call TAU_ENABLE_TRACKING_POWER();
        

**Fortran :**

::

    import pytau

    pytau.enableTrackingPowerHeadroom()
        

See Also
========

?, ?, ?, ?

TAU\_DISABLE\_TRACKING\_POWER
3
TAU\_DISABLE\_TRACKING\_POWER
Disables power headroom tracking
C/C++:
TAU\_DISABLE\_TRACKING\_POWER
Fortran:
TAU\_DISABLE\_TRACKING\_POWER
Description
===========

``TAU_DISABLE_TRACKING_POWER()`` disables power tracking.

Example
=======

**C/C++ :**

::

    TAU_DISABLE_TRACKING_POWER();
        

**Fortran :**

::

    call TAU_DISABLE_TRACKING_POWER()
        

**Python:**

::

    import pytau

    pytau.disableTrackingPowerHeadroom()
        

See Also
========

?, ?, ?, ?

TAU\_TRACK\_MEMORY
3
TAU\_TRACK\_MEMORY
Initializes memory tracking system
C/C++:
TAU\_TRACK\_MEMORY
Fortran:
TAU\_TRACK\_MEMORY
Description
===========

For memory profiling, there are two modes of operation: 1) the user
explicitly inserts TAU\_TRACK\_MEMORY\_HERE() calls in the source code
and the memory event is triggered at those locations, and 2) the user
enables tracking memory by calling TAU\_TRACK\_MEMORY() and an interrupt
is generated every 10 seconds and the memory event is triggered with the
current value. Also, this interrupt interval can be changed by calling
TAU\_SET\_INTERRUPT\_INTERVAL(value). The tracking of memory events in
both cases can be explictly enabled or disabled by calling the macros
TAU\_ENABLE\_TRACKING\_MEMORY() or TAU\_DISABLE\_TRACKING\_MEMORY()
respectively.

Example
=======

**C/C++ :**

::

    TAU_TRACK_MEMORY();      
        

**Fortran :**

::

    call TAU_TRACK_MEMORY()
        

**Python:**

::

    import pytau

    pytau.trackMemory()
        

See Also
========

?, ?, ?, ?, ?

TAU\_TRACK\_MEMORY\_HERE
3
TAU\_TRACK\_MEMORY\_HERE
Triggers memory tracking at a given execution point
C/C++:
TAU\_TRACK\_MEMORY\_HERE
Fortran:
TAU\_TRACK\_MEMORY\_HERE
Description
===========

Triggers memory tracking at a given execution point

Example
=======

**C/C++ :**

::

    int main(int argc, char **argv) {
      TAU_PROFILE("main()", " ", TAU_DEFAULT);
      TAU_PROFILE_SET_NODE(0);

      TAU_TRACK_MEMORY_HERE();

      int *x = new int[5*1024*1024];
      TAU_TRACK_MEMORY_HERE();
      return 0;
    }
        

**Fortran :**

::

    INTEGER, ALLOCATABLE :: STORAGEARY(:)
    allocate(STORAGEARY(1:999), STAT=IERR)

    ! if we wish to record a sample of the heap memory 
    ! utilization at this point, invoke the following call:
    call TAU_TRACK_MEMORY_HERE()

        

**Python:**

::

    import pytau

    pytau.trackMemoryHere()
            

See Also
========

?

TAU\_ENABLE\_TRACKING\_MEMORY\_HEADROOM
3
TAU\_ENABLE\_TRACKING\_MEMORY\_HEADROOM
Enables memory headroom tracking
C/C++:
TAU\_ENABLE\_TRACKING\_MEMORY\_HEADROOM
Fortran:
TAU\_ENABLE\_TRACKING\_MEMORY\_HEADROOM
Description
===========

``TAU_ENABLE_TRACKING_MEMORY_HEADROOM()`` enables memory headroom
tracking after a ``TAU_DISABLE_TRACKING_MEMORY_HEADROOM()``.

Example
=======

**C/C++ :**

::

    TAU_DISABLE_TRACKING_MEMORY_HEADROOM();
    /* do some work */
    ...
    /* re-enable tracking memory headroom */
    TAU_ENABLE_TRACKING_MEMORY_HEADROOM();
        

**Fortran :**

::

    call TAU_ENABLE_TRACKING_MEMORY_HEADROOM();
        

**Fortran :**

::

    import pytau

    pytau.enableTrackingMemoryHeadroom()
        

See Also
========

?, ?, ?, ?

TAU\_DISABLE\_TRACKING\_MEMORY\_HEADROOM
3
TAU\_DISABLE\_TRACKING\_MEMORY\_HEADROOM
Disables memory headroom tracking
C/C++:
TAU\_DISABLE\_TRACKING\_MEMORY\_HEADROOM
Fortran:
TAU\_DISABLE\_TRACKING\_MEMORY\_HEADROOM
Description
===========

``TAU_DISABLE_TRACKING_MEMORY_HEADROOM()`` disables memory headroom
tracking.

Example
=======

**C/C++ :**

::

    TAU_DISABLE_TRACKING_MEMORY_HEADROOM();
        

**Fortran :**

::

    call TAU_DISABLE_TRACKING_MEMORY_HEADROOM()
        

**Python:**

::

    import pytau

    pytau.disableTrackingMemoryHeadroom()
        

See Also
========

?, ?, ?, ?

TAU\_TRACK\_MEMORY\_HEADROOM
3
TAU\_TRACK\_MEMORY\_HEADROOM
Track the headroom (amount of memory for a process to grow) by
periodically interrupting the program
C/C++:
TAU\_TRACK\_MEMORY\_HEADROOM
Fortran:
TAU\_TRACK\_MEMORY\_HEADROOM
Description
===========

Tracks the amount of memory available for the process before it runs out
of free memory on the heap. This call sets up a signal handler that is
invoked every 10 seconds by an interrupt (this interval may be altered
by using the ``TAU_SET_INTERRUPT_INTERVAL`` call). Inside the interrupt
handler, TAU evaluates how much memory it can allocate and associates it
with the callstack using the TAU context events (See ?). The user can
vary the size of the callstack by setting the environment variable
``TAU_CALLPATH_DEPTH`` (default is 2). This call is useful on machines
like IBM BG/L where no virtual memory (or paging using the swap space)
is present. The amount of heap memory available to the program is
limited by the amount of available physical memory. TAU executes a
series of malloc calls with a granularity of 1MB and determines the
amount of memory available for the program to grow.

Example
=======

**C/C++ :**

::

    TAU_TRACK_MEMORY_HEADROOM();
        

**Fortran :**

::

    call TAU_TRACK_MEMORY_HEADROOM()
        

**Python:**

::

    import pytau

    pytau.trackMemoryHeadroom()
        

See Also
========

?, ?, ?, ?, ?

TAU\_TRACK\_MEMORY\_HEADROOM\_HERE
3
TAU\_TRACK\_MEMORY\_HEADROOM\_HERE
Takes a sample of the amount of memory available at a given point.
C/C++:
TAU\_TRACK\_MEMORY\_HEADROOM\_HERE
Fortran:
TAU\_TRACK\_MEMORY\_HEADROOM\_HERE
Description
===========

Instead of relying on a periodic interrupt to track the amount of memory
available to grow, this call may be used to take a sample at a given
location in the source code. Context events are used to track the amount
of memory headroom.

Example
=======

**C/C++ :**

::

    ary = new double [1024*1024*50];
    TAU_TRACK_MEMORY_HEADROOM_HERE();
        

**Fortran :**

::

    INTEGER, ALLOCATABLE :: STORAGEARY(:)
    allocate(STORAGEARY(1:999), STAT=IERR)
    TAU_TRACK_MEMORY_HEADROOM_HERE();
        

**Python:**

::

    import pytau

    pytau.trackMemoryHeadroomHere()
            

See Also
========

?

TAU\_SET\_INTERRUPT\_INTERVAL
3
TAU\_SET\_INTERRUPT\_INTERVAL
Change the inter-interrupt interval for tracking memory and headroom
C/C++:
TAU\_SET\_INTERRUPT\_INTERVAL
int
value
Fortran:
TAU\_SET\_INTERRUPT\_INTERVAL
integer
value
Description
===========

Set the interrupt interval for tracking memory and headroom (See ? and
?). By default an inter-interrupt interval of 10 seconds is used in TAU.
This call allows the user to set it to a different value specified by
the argument value.

Example
=======

**C/C++ :**

::

    TAU_SET_INTERRUPT_INTERVAL(2)
    /* invokes the interrupt handler for memory every 2s */
        

**Fortran :**

::

    call TAU_SET_INTERRUPT_INTERVAL(2)
        

**Python:**

::

    import pytau

    pytau.setInterruptTnterval(2)
            

See Also
========

?, ?

CT
3
CT
Returns the type information for a variable
C/C++:
CT
<type>
variable
Description
===========

The ``CT`` macro returns the runtime type information string of a
variable. This is useful in constructing the type parameter of the
``TAU_PROFILE`` macro. For templates, the type information can be
constructed using the type of the return and the type of each of the
arguments (parameters) of the template. The example in the following
macro will clarify this.

Example
=======

**C/C++ :**

::

    TAU_PROFILE("foo::memberfunc()", CT(*this), TAU_DEFAULT);
        

See Also
========

?, ?, ?

TAU\_TYPE\_STRING
3
TAU\_TYPE\_STRING
Creates a type string
C++:
TAU\_TYPE\_STRING
string &
variable
string &
type\_string
Description
===========

This macro assigns the string constructed in type\_string to the
variable. The + operator and the CT macro can be used to construct the
type string of an object. This is useful in identifying templates
uniquely, as shown below.

Example
=======

**C++ :**

::

    template<class PLayout>
    ostream& operator<<(ostream& out, const ParticleBase<PLayout>& P) {
      TAU_TYPE_STRING(taustr, "ostream (ostream, " + CT(P) + " )");
      TAU_PROFILE("operator<<()"taustr, TAU_PARTICLE | TAU_IO);
      ... 
    }
        

When PLayout is instantiated with " ``UniformCartesian<3U, double>``
",this generates the unique template name:

::

    operator<<() ostream const 
    ParticleBase<UniformCartesian<3U, double> > )
        

The following example illustrates the usage of the CT macro to extract
the name of the class associated with the given object using CT(\*this);

::

    template<class PLayout>
    unsigned ParticleBase<PLayout7>::GetMessage(Message& msg, int node) {
      TAU_TYPE_STRING(taustr, CT(*this) + "unsigned (Message, int)");
      TAU_PROFILE("ParticleBase::GetMessage()", taustr, TAU_PARTICLE);
      ...
    }
        

When PLayout is instantiated with " ``UniformCartesian<3U,
    double>`` ",this generates the unique template name:

::

    ParticleBase::GetMessage() ParticleBase<UniformCartesian<3U, 
    double> > unsigned (Message, int)
        

See Also
========

?, ?, ?

TAU\_DB\_DUMP
3
TAU\_DB\_DUMP
Dumps the profile database to disk
C/C++:
TAU\_DB\_DUMP
Fortran:
TAU\_DB\_DUMP
Description
===========

Dumps the profile database to disk. The format of the files is the same
as regular profiles, they are simply prefixed with "dump" instead of
"profile".

Example
=======

**C/C++ :**

::

    TAU_DB_DUMP();
        

**Fortran :**

::

    call TAU_DB_DUMP()
        

See Also
========

?, ?, ?, ?, ?, ?, ?

TAU\_DB\_MERGED\_DUMP
3
TAU\_DB\_MERGED\_DUMP
Dumps the profile database to disk
C/C++:
TAU\_DB\_MERGED\_DUMP
Fortran:
TAU\_DB\_MERGED\_DUMP
Description
===========

Dumps the profile database to disk. The format of the files is the same
as merged profiles: tauprofile.xml

Example
=======

**C/C++ :**

::

    TAU_DB_MERGED_DUMP();
        

**Fortran :**

::

    call TAU_DB_MERGED_DUMP()
        

See Also
========

?, ?, ?, ?, ?, ?, ?

TAU\_DB\_DUMP\_INCR
3
TAU\_DB\_DUMP\_INCR
Dumps profile database into timestamped profiles on disk
C/C++:
TAU\_DB\_DUMP\_INCR
Description
===========

This is similar to the TAU\_DB\_DUMP macro but it produces dump files
that have a timestamp in their names. This allows the user to record
timestamped incremental dumps as the application executes.

Example
=======

**C/C++ :**

::

    TAU_DB_DUMP_INCR();
        

**Python:**

::

    import pytau

    pytau.dbDumpIncr("prefix")
        

See Also
========

?, ?, ?, ?, ?, ?, ?

TAU\_DB\_DUMP\_PREFIX
3
TAU\_DB\_DUMP\_PREFIX
Dumps the profile database into profile files with a given prefix
C/C++:
TAU\_DB\_DUMP\_PREFIX
char \*
prefix
Fortran:
TAU\_DB\_DUMP\_PREFIX
character
prefix
(size)
Description
===========

The ``TAU_DB_DUMP_PREFIX`` macro dumps all profile data to disk and
records a checkpoint or a snapshot of the profile statistics at that
instant. The dump files are named <prefix>.<node>.<context>.<thread>. If
prefix is "profile", the files are named profile.0.0.0, etc. and may be
read by paraprof/pprof tools as the application executes.

Example
=======

**C/C++ :**

::

    TAU_DB_DUMP_PREFIX("prefix");      
        

**Fortran :**

::

    call TAU_DB_DUMP_PREFIX("prefix")
        

**Python :**

::

    import pytau

    pytau.dbDump("prefix")
        

See Also
========

?

TAU\_DB\_DUMP\_PREFIX\_TASK
3
TAU\_DB\_DUMP\_PREFIX\_TASK
Dumps the profile database into profile files with a given task
C/C++:
TAU\_DB\_DUMP\_PREFIX\_TASK
char \*
PREFIX\_TASK
Fortran:
TAU\_DB\_DUMP\_PREFIX\_TASK
character
prefix
(size)
integer
task
(size)
Description
===========

The ``TAU_DB_DUMP_PREFIX_TASK`` macro dumps all profile data to disk and
records a checkpoint or a snapshot of the profile statistics on a
particular task at that instant. The dump files are named
<prefix>.<node>.<context>.<thread>. If prefix is "profile", the files
are named profile.0.0.0, etc. and may be read by paraprof/pprof tools as
the application executes.

Example
=======

**C/C++ :**

::

    TAU_DB_DUMP_PREFIX_TASK("PREFIX", taskid);      
        

**Fortran :**

::

    call TAU_DB_DUMP_PREFIX_TASK("PREFIX", taskid)
        

**Python :**

::

    import pytau

    pytau.dbDump("PREFIX", taskid)
        

See Also
========

?

TAU\_DB\_PURGE
3
TAU\_DB\_PURGE
Purges the performance data.
C/C++:
TAU\_DB\_PURGE
Description
===========

Purges the performance data collected so far.

Example
=======

**C/C++ :**

::

    TAU_DB_PURGE();
        

See Also
========

?

TAU\_DUMP\_FUNC\_NAMES
3
TAU\_DUMP\_FUNC\_NAMES
Dumps function names to disk
C/C++:
TAU\_DUMP\_FUNC\_NAMES
Description
===========

This macro writes the names of active functions to a file named
dump\_functionnames\_<node>.<context>.

Example
=======

**C/C++ :**

::

    TAU_DUMP_FUNC_NAMES();
        

**Python:**

::

    import pytau

    pytau.dumpFuncNames()
        

See Also
========

?, ?, ?

TAU\_DUMP\_FUNC\_VALS
3
TAU\_DUMP\_FUNC\_VALS
Dumps performance data for given functions to disk.
C/C++:
TAU\_DUMP\_FUNC\_VALS
char \*\*
inFuncs
int
numFuncs
Description
===========

``TAU_DUMP_FUNC_VALS`` writes the data associated with the routines
listed in inFuncs to disk. The number of routines is specified by the
user in numFuncs.

Example
=======

**C/C++ :**

::


        

See Also
========

?, ?, ?

TAU\_DUMP\_FUNC\_VALS\_INCR
3
TAU\_DUMP\_FUNC\_VALS\_INCR
Dumps function values with a timestamp
C/C++:
TAU\_DUMP\_FUNC\_VALS\_INCR
char \*\*
inFuncs
int
numFuncs
Description
===========

Similar to ``TAU_DUMP_FUNC_VALS``. This macro creates an incremental
selective dump and dumps the results with a date stamp to the filename
such as sel\_dump\_\_Thu-Mar-28-16:30:48-2002\_\_.0.0.0. In this manner
the previous ``TAU_DUMP_FUNC_VALS_INCR(...)`` are not overwritten
(unless they occur within a second).

Example
=======

**C/C++ :**

::

    const char **inFuncs;
    /* The first dimension is functions, and the second dimension is counters */
    double **counterExclusiveValues;
    double **counterInclusiveValues;
    int *numOfCalls;
    int *numOfSubRoutines;
    const char **counterNames;
    int numOfCouns;

    TAU_GET_FUNC_VALS(inFuncs, 2,
      counterExclusiveValues,
      counterInclusiveValues,
      numOfCalls,
      numOfSubRoutines,
      counterNames,
      numOfCouns);

    TAU_DUMP_FUNC_VALS(inFuncs, 2);
        

**Python:**

::

    import pytau

    pytau.dumpFuncValsIncr("foo", "bar", "bar2")
            

See Also
========

?, ?, ?

TAU\_PROFILE\_STMT
3
TAU\_PROFILE\_STMT
Executes a statement only when TAU is used.
C/C++:
TAU\_PROFILE\_STMT
statement
statement
Description
===========

``TAU_PROFILE_STMT`` executes a statement, or declares a variable that
is used only during profiling or for execution of a statement that takes
place only when the instrumentation is active. When instrumentation is
inactive (i.e., when profiling and tracing are turned off as described
in Chapter 2), all macros are defined as null.

Example
=======

**C/C++ :**

::

    TAU_PROFILE_STMT(T obj;); // T is a template parameter)
    TAU_TYPE_STRING(str, "void () " + CT(obj) );
        

TAU\_PROFILE\_CALLSTACK
3
TAU\_PROFILE\_CALLSTACK
Generates a callstack trace at a given location.
C/C++:
TAU\_PROFILE\_CALLSTACK
Description
===========

When TAU is configured with ``-PROFILECALLSTACK`` configuration option,
and this call is invoked, a callpath trace is generated. A GUI for
viewing this trace is included in TAU's utils/csUI directory. This
option is deprecated.

Example
=======

**C/C++ :**

::

    TAU_PROFILE_CALLSTACK();
        

TAU\_TRACE\_RECVMSG
3
TAU\_TRACE\_RECVMSG
Traces a receive operation
C/C++:
TAU\_TRACE\_RECVMSG
int
tag
int
source
int
length
Fortran:
TAU\_TRACE\_RECVMSG
integer
tag
integer
source
integer
length
Description
===========

``TAU_TRACE_RECVMSG`` traces a receive operation where tag represents
the type of the message received from the source process.

*NOTE:* When TAU is configured to use MPI (-mpiinc=<dir> -mpilib=<dir>),
the ``TAU_TRACE_RECVMSG`` and ``TAU_TRACE_SENDMSG`` macros are not
required. The wrapper interposition library in

::

    $(TAU_MPI_LIBS)

uses these macros internally for logging messages.

Example
=======

**C/C++ :**

::

    if (pid == 0) {
      TAU_TRACE_SENDMSG(currCol, sender, ncols * sizeof(T));
      MPI_Send(vctr2, ncols * sizeof(T), MPI_BYTE, sender, 
               currCol, MPI_COMM_WORLD);
    } else {
      MPI_Recv(&ans, sizeof(T), MPI_BYTE, MPI_ANY_SOURCE, 
               MPI_ANY_TAG,MPI_COMM_WORLD, &stat);
      MPI_Get_count(&stat, MPI_BYTE, &recvcount);
      TAU_TRACE_RECVMSG(stat.MPI_TAG, stat.MPI_SOURCE, recvcount);
    }
        

**Fortran :**

::

    call TAU_TRACE_RECVMSG(tag, source, length)
    call TAU_TRACE_SENDMSG(tag, destination, length)
        

See Also
========

?

TAU\_TRACE\_SENDMSG
3
TAU\_TRACE\_SENDMSG
Traces a receive operation
C/C++:
TAU\_TRACE\_SENDMSG
int
tag
int
source
int
length
Fortran:
TAU\_TRACE\_SENDMSG
integer
tag
integer
source
integer
length
Description
===========

``TAU_TRACE_SENDMSG`` traces an inter-process message communication when
a tagged message is sent to a destination process.

*NOTE:* When TAU is configured to use MPI (-mpiinc=<dir> -mpilib=<dir>),
the ``TAU_TRACE_SENDMSG`` and ``TAU_TRACE_SENDMSG`` macros are not
required. The wrapper interposition library in

::

    $(TAU_MPI_LIBS)

uses these macros internally for logging messages.

Example
=======

**C/C++ :**

::

    if (pid == 0) {
      TAU_TRACE_SENDMSG(currCol, sender, ncols * sizeof(T));
      MPI_Send(vctr2, ncols * sizeof(T), MPI_BYTE, sender, 
               currCol, MPI_COMM_WORLD);
    } else {
      MPI_Recv(&ans, sizeof(T), MPI_BYTE, MPI_ANY_SOURCE, 
               MPI_ANY_TAG,MPI_COMM_WORLD, &stat);
      MPI_Get_count(&stat, MPI_BYTE, &recvcount);
      TAU_TRACE_RECVMSG(stat.MPI_TAG, stat.MPI_SOURCE, recvcount);
    }
        

**Fortran :**

::

    call TAU_TRACE_RECVMSG(tag, source, length)
    call TAU_TRACE_SENDMSG(tag, destination, length)
        

See Also
========

?

TAU\_PROFILE\_PARAM1L
3
TAU\_PROFILE\_PARAM1L
Creates a snapshot of the current apllication profile
C/C++:
TAU\_PROFILE\_PARAM1L
long
number
char\*
name
Fortran:
TAU\_PROFILE\_PARAM1L
char\*
name
integer
number
integer
length
Description
===========

Track the a given numerial parameter to a function and records each
value as a seperate event. ``number`` is the parameter to be tracked.
``name`` is the name of this event.

Example
=======

**C/C++:**

::

    int f1(int x)
    {
      TAU_PROFILE("f1()", "", TAU_USER);
      TAU_PROFILE_PARAM1L((long) x, "x");
        ...

**Fortran:**

::

     subroutine ITERATION(val)
      integer val
      integer profiler(2) / 0, 0 /
      save profiler

      call TAU_PROFILE_TIMER(profiler, 'INTERATION')
      call TAU_PROFILE_START(profiler)

        call TAU_PROFILE_PARAM1L('value', val, 4) 

        ....

        call TAU_PROFILE_STOP(profiler)
      return
    end

See Also
========

?

TAU\_PROFILE\_SNAPSHOT
3
TAU\_PROFILE\_SNAPSHOT
Creates a snapshot of the current apllication profile
C/C++:
TAU\_PROFILE\_SNAPSHOT
char\*
name
Fortran:
TAU\_PROFILE\_SNAPSHOT
char\*
name
integer
length
Description
===========

``TAU_PROFILE_SNAPSHOT`` writes a snapshot profile representing the
program's execution up to this point. These file are written the system
as snapshot.[node].[context].[thread] format. They can be merged by
appending one to another. Uploading a snapshot to a PerfDMF database or
packing them into a PPK file will condense them to a single profile (the
last one).

Examples
========

C/C++:

::

    TAU_PROFILE_SNAPSHOT(name);

Fortran:

::

    TAU_PROFILE_SNAPSHOT(name, length);

Python:

::

    import pytau;

    pytau.snapshot("name")

See Also
========

?

TAU\_PROFILE\_SNAPSHOT\_1L
3
TAU\_PROFILE\_SNAPSHOT\_1L
Creates a snapshot of the current apllication profile
C/C++:
TAU\_PROFILE\_SNAPSHOT\_1L
char\*
name
int
number
Fortran:
TAU\_PROFILE\_SNAPSHOT\_1L
char\*
name
integer
number
integer
length
Description
===========

Calls ``TAU_PROFILE_SNAPSHOT`` giving it the as a name the name with a
number appended.

See Also
========

?

TAU\_PROFILER\_CREATE
TAU\_PROFILER\_CREATE
Creates a profiler object referenced as a standard pointer
C/C++:
TAU\_PROFILER\_CREATE
Timer
timer
char\* or string&
function\_name
char\* or string&
type
taugroup\_t
group
description
===========

``TAU_PROFILER_CREATE`` creates a timer the that can be controlled by
the Timer pointer object.

The TAU\_PROFILER\_\* API is intended for applications to easily layer
their legacy timing measurements APIs on top of TAU, Unlike other TAU
API calls (TAU\_PROFILE\_TIMER) that are statically expanded in the
source code, these calls allocate TAU entities on the heap. So the
pointer to the TAU timer may be used as a handle to access the TAU
performance data.

example
=======

>\ **C/C++:**

::

    void *ptr;
    TAU_PROFILER_CREATE(ptr, "foo","", TAU_USER);

    TAU_PROFILER_START(ptr);
    foo(2);
    TAU_PROFILER_STOP(ptr); 

>\ **Python:**

::

    import pytau
    ptr = pytau.profileTimer("foo")

    pytau.start(ptr)
    foo(2)
    pytau.stop(ptr) 

See Also
========

? ? ? ? ? ? ?

TAU\_CREATE\_TASK
TAU\_CREATE\_TASK
Creates a task id.
C/C++:
TAU\_CREATE\_TASK
Integer
taskid
description
===========

``TAU_CREATE_TASK`` creates a task with id 'taskid' this task is an
independent event stream for which Profiler objects can be started and
stop on. TAU will increment the taskids as needed an write out profiles
and traces from the task as if they were thread.

example
=======

>\ **C/C++:**

::

    void *ptr;
    int taskid;
    TAU_PROFILER_CREATE(ptr, "foo","", TAU_USER);
    TAU_CREATE_TASK(taskid);
    TAU_PROFILER_START_TASK(ptr,taskid);
    foo(2);
    TAU_PROFILER_STOP_TASK(ptr,taskid); 

See Also
========

? ? ? ? ? ? ?

TAU\_PROFILER\_START
TAU\_PROFILER\_START
starts a profiler object created by
C/C++:
TAU\_PROFILER\_START
Timer
timer
description
===========

``TAU_PROFILER_START``\ starts a profiler timer by passing the pointer
created by the ?.

example
=======

>\ **C/C++:**

::

    void *ptr;
    TAU_PROFILER_CREATE(ptr, "foo","", TAU_USER);

    TAU_PROFILER_START(ptr);
    foo(2);
    TAU_PROFILER_STOP(ptr); 

>\ **Python:**

::

    import pytau
    ptr = pytau.profileTimer("foo")

    pytau.start(ptr)
    foo(2)
    pytau.stop(ptr) 

See Also
========

? ? ? ? ? ? ?

TAU\_PROFILER\_START\_TASK
TAU\_PROFILER\_START\_TASK
Starts a profiler object created by
on a given task.
C/C++:
TAU\_PROFILER\_START\_TASK
Timer
timer
description
===========

``TAU_PROFILER_START_TASK``\ starts a profiler timer on a task by
passing the pointer created by the ? and a task created by ? on a given
task.

example
=======

>\ **C/C++:**

::

    void *ptr;
    int taskid;
    TAU_PROFILER_CREATE(ptr, "foo","", TAU_USER);
    TAU_CREATE_TASK(taskid);
    TAU_PROFILER_START_TASK(ptr,taskid);
    foo(2);
    TAU_PROFILER_STOP_TASK(ptr,taskid); 

See Also
========

? ? ? ? ? ? ?

TAU\_PROFILER\_STOP
TAU\_PROFILER\_STOP
stops a profiler object created by
C/C++:
TAU\_PROFILER\_STOP
Timer
timer
description
===========

``TAU_PROFILER_STOP``\ stops a profiler timer by passing the pointer
created by the ?.

example
=======

>\ **C/C++:**

::

    void *ptr;
    TAU_PROFILER_CREATE(ptr, "foo","", TAU_USER);

    TAU_PROFILER_START(ptr);
    foo(2);
    TAU_PROFILER_STOP(ptr); 

>\ **Python:**

::

    import pytau
    ptr = pytau.profileTimer("foo")

    pytau.start(ptr)
    foo(2)
    pytau.stop(ptr) 

See Also
========

? ? ? ? ? ? ?

TAU\_PROFILER\_STOP\_TASK
TAU\_PROFILER\_STOP\_TASK
Stops a profiler object on a task
C/C++:
TAU\_PROFILER\_STOP\_TASK
Timer
timer
description
===========

``TAU_PROFILER_STOP_TASK``\ STOPs a profiler timer on a task by passing
the pointer created by the ? and a task created by ?.

example
=======

>\ **C/C++:**

::

    void *ptr;
    int taskid;
    TAU_PROFILER_CREATE(ptr, "foo","", TAU_USER);
    TAU_CREATE_TASK(taskid);
    TAU_PROFILER_START_TASK(ptr,taskid);
    foo(2);
    TAU_PROFILER_STOP_TASK(ptr,taskid); 

See Also
========

? ? ? ? ? ? ?

TAU\_PROFILER\_GET\_CALLS
TAU\_PROFILER\_GET\_CALLS
Gets the number of times this timer, created by
, is started.
C/C++:
TAU\_PROFILER\_GET\_CALLS
Timer
timer
long&
calls
description
===========

``TAU_PROFILER_GET_CALLS`` returns the number of times this timer is
started (ie. The number of times the section of code being profiled was
executed).

example
=======

>\ **C/C++:**

::

    void *ptr;
    TAU_PROFILER_CREATE(ptr, "foo","", TAU_USER);

    TAU_PROFILER_START(ptr);
    foo(2);
    long calls;
    TAU_PROFILER_GET_CALLS(ptr, &calls); 

See Also
========

? ? ? ? ? ? ?

TAU\_PROFILER\_GET\_CALLS\_TASK
TAU\_PROFILER\_GET\_CALLS\_TASK
Gets the number of times this timer, created by
, is started on a given task.
C/C++:
TAU\_PROFILER\_GET\_CALLS\_TASK
Timer
timer
long&
calls
int
taskid
description
===========

``TAU_PROFILER_GET_CALLS_TASK`` returns the number of times this timer
is started (ie. The number of times the section of code being profiled
was executed) on a given task.

example
=======

>\ **C/C++:**

::

    void *ptr;
    int taskid;
    TAU_PROFILER_CREATE(ptr, "foo","", TAU_USER);
    TAU_CREATE_TASK(taskid);
    TAU_PROFILER_START_TASK(ptr, taskid);
    foo(2);
    long calls;
    TAU_PROFILER_GET_CALLS_TASK(ptr, &calls, taskid); 

See Also
========

? ? ? ? ? ? ?

TAU\_PROFILER\_GET\_CHILD\_CALLS
TAU\_PROFILER\_GET\_CHILD\_CALLS
Gets the number of calls made while this timer was running
C/C++:
TAU\_PROFILER\_GET\_CHILD\_CALLS
Timer
timer
long&
calls
description
===========

``TAU_PROFILER_GET_CHILD_CALLS`` Gets the number of timers started while
``timer`` was running. This is non-recursive, only timers started
directly count.

example
=======

>\ **C/C++:**

::

    void *ptr;
    TAU_PROFILER_CREATE(ptr, "foo","", TAU_USER);

    TAU_PROFILER_START(ptr);
    foo(2);
    TAU_PROFILER_STOP(ptr);

    long calls;
    TAU_PROFILER_GET_CHILD_CALLS(ptr, &calls); 

See Also
========

? ? ? ? ? ? ?

TAU\_PROFILER\_GET\_CHILD\_CALLS\_TASK
TAU\_PROFILER\_GET\_CHILD\_CALLS\_TASK
Gets the number of child call for this timer, created by
, is started on a task.
C/C++:
TAU\_PROFILER\_GET\_CHILD\_CALLS\_TASK
Timer
timer
long&
child\_calls
int
taskid
description
===========

``TAU_PROFILER_GET_CHILD_CALLS_TASK`` returns the number of times this
timer is started (ie. The number of times the section of code being
profiled was executed).

example
=======

>\ **C/C++:**

::

    void *ptr;
    int taskid;
    TAU_PROFILER_CREATE(ptr, "foo","", TAU_USER);
    TAU_CREATE_TASK(taskid);
    TAU_PROFILER_START_TASK(ptr, taskid);
    foo(2);
    long child_calls;
    TAU_PROFILER_GET_CHILD_CALLS_TASK(ptr, &child_calls, taskid); 

See Also
========

? ? ? ? ? ? ?

TAU\_PROFILER\_GET\_INCLUSIVE\_VALUES
TAU\_PROFILER\_GET\_INCLUSIVE\_VALUES
Returns the inclusive amount of a metric spend by this timer.
C/C++:
TAU\_PROFILER\_GET\_INCLUSIVE\_VALUES
Timer
timer
double&
incl
description
===========

``TAU_PROFILER_GET_INCLUSIVE_VALUES`` Returns the inclusive amount of a
metric spend while this timer was running (and any subsequent timers
called from this timer.)

example
=======

>\ **C/C++:**

::

    void *ptr;
    TAU_PROFILER_CREATE(ptr, "foo","", TAU_USER);

    TAU_PROFILER_START(ptr);
    foo(2);
    TAU_PROFILER_STOP(ptr);

    double incl[TAU_MAX_COUNTERS];
    TAU_PROFILER_GET_INCLUSIVE_VALUES(ptr, &incl); 

See Also
========

? ? ? ? ? ? ?

TAU\_PROFILER\_GET\_INCLUSIVE\_VALUES\_TASK
TAU\_PROFILER\_GET\_INCLUSIVE\_VALUES\_TASK
Returns the inclusive amount of a metric spend by this timer on a given
task.
C/C++:
TAU\_PROFILER\_GET\_INCLUSIVE\_VALUES\_TASK
Timer
timer
double&
incl
int
taskid
description
===========

``TAU_PROFILER_GET_INCLUSIVE_VALUES_TASK`` Returns the inclusive amount
of a metric spend while this timer was running (and any subsequent
timers called from this timer) on a given task.

example
=======

>\ **C/C++:**

::

    void *ptr;
    int taskid;
    TAU_PROFILER_CREATE(ptr, "foo","", TAU_USER);
    TAU_CREATE_TASK(taskid);
    TAU_PROFILER_START(ptr);
    foo(2);
    TAU_PROFILER_STOP(ptr);

    double incl[TAU_MAX_COUNTERS];
    TAU_PROFILER_GET_INCLUSIVE_VALUES_TASK(ptr, &incl, taskid); 

See Also
========

? ? ? ? ? ? ?

TAU\_PROFILER\_GET\_EXCLUSIVE\_VALUES
TAU\_PROFILER\_GET\_EXCLUSIVE\_VALUES
Returns the exclusive amount of a metric spend by this timer.
C/C++:
TAU\_PROFILER\_GET\_EXCLUSIVE\_VALUES
Timer
timer
double&
excl
description
===========

``TAU_PROFILER_GET_EXCLUSIVE_VALUES`` Returns the exclusive amount of
the metric spend while this timer was running (and while no other
subsequent timers was running.)

example
=======

>\ **C/C++:**

::

    void *ptr;
    TAU_PROFILER_CREATE(ptr, "foo","", TAU_USER);

    TAU_PROFILER_START(ptr);
    foo(2);
    TAU_PROFILER_STOP(ptr);

    double excl[TAU_MAX_COUNTERS];
    TAU_PROFILER_GET_EXCLUSIVE_VALUES(ptr, &excl); 

See Also
========

? ? ? ? ? ? ?

TAU\_PROFILER\_GET\_EXCLUSIVE\_VALUES\_TASK
TAU\_PROFILER\_GET\_EXCLUSIVE\_VALUES\_TASK
Returns the exclusive amount of a metric spend by this timer on a given
task.
C/C++:
TAU\_PROFILER\_GET\_EXCLUSIVE\_VALUES\_TASK
Timer
timer
double&
excl
int
taskid
description
===========

``TAU_PROFILER_GET_EXCLUSIVE_VALUES_TASK`` Returns the exclusive amount
of the metric spend while this timer was running (and while no other
subsequent timers was running) on a given task.

example
=======

>\ **C/C++:**

::

    void *ptr;
    int taskid;
    TAU_PROFILER_CREATE(ptr, "foo","", TAU_USER);
    TAU_CREATE_TASK(taskid);
    TAU_PROFILER_START(ptr);
    foo(2);
    TAU_PROFILER_STOP(ptr);

    double excl[TAU_MAX_COUNTERS];
    TAU_PROFILER_GET_EXCLUSIVE_VALUES_TASK(ptr, &excl, taskid); 

See Also
========

? ? ? ? ? ? ?

TAU\_PROFILER\_GET\_COUNTER\_INFO
TAU\_PROFILER\_GET\_COUNTER\_INFO
Returns information about all the timers created.
C/C++:
TAU\_PROFILER\_GET\_COUNTER\_INFO
const char \*
counters
int &
num\_counters
description
===========

``TAU_PROFILER_GET_COUNTER_INFO`` Gets the number of counters created
and an array of the counters containing information about the counters.

example
=======

>\ **C/C++:**

::

    void *ptr;
    TAU_PROFILER_CREATE(ptr, "foo","", TAU_USER);

    TAU_PROFILER_START(ptr);
    foo(2);
    TAU_PROFILER_STOP(ptr);

    const char **counters;
    int numcounters;

    TAU_PROFILER_GET_COUNTER_INFO(&counters, &numcounters);
    printf("numcounters = %d\n", numcounters);
    for (j = 0; j < numcounters ; j++) 
    {
        printf(">>>");
        printf("counter [%d] = %s\n", j, counters[j]);
    }

See Also
========

? ? ? ? ? ? ?

TAU\_PROFILER\_GET\_COUNTER\_INFO\_TASK
TAU\_PROFILER\_GET\_COUNTER\_INFO\_TASK
Returns information about all the timers created on a task.
C/C++:
TAU\_PROFILER\_GET\_COUNTER\_INFO\_TASK
const char \*
counters
int &
num\_counters
int
taskid
description
===========

``TAU_PROFILER_GET_COUNTER_INFO_TASK`` Gets the number of counters
created and an array of the counters containing information about the
counters on a given task.

example
=======

>\ **C/C++:**

::

    void *ptr;
    int taskid;
    TAU_PROFILER_CREATE(ptr, "foo","", TAU_USER);
    TAU_CREATE_TASK(taskid);
    TAU_PROFILER_START_TASK(ptr, taskid);
    foo(2);
    TAU_PROFILER_STOP_TASK(ptr, taskid);

    const char **counters;
    int numcounters;

    TAU_PROFILER_GET_COUNTER_INFO_TASK(&counters, &numcounters, taskid);
    printf("numcounters = %d\n", numcounters);
    for (j = 0; j < numcounters ; j++) 
    {
        printf(">>>");
        printf("counter [%d] = %s\n", j, counters[j]);
    }

See Also
========

? ? ? ? ? ? ?

TAU\_QUERY\_DECLARE\_EVENT
TAU\_QUERY\_DECLARE\_EVENT
Returns a event handle.
C/C++:
TAU\_QUERY\_DECLARE\_EVENT
void \*
event
description
===========

``TAU_QUERY_DECLARE_EVENT`` Creates a event handle for querying TAU
events.

example
=======

>\ **C/C++:**

::

    char[100] str;
    TAU_QUERY_DECLARE_EVENT(event);
    TAU_QUERY_GET_CURRENT_EVENT(event);
    TAU_QUERY_GET_EVENT_NAME(event, str);

    printf("current event is: %d.\n", str);

See Also
========

? ? ? ?

TAU\_QUERY\_GET\_CURRENT\_EVENT
TAU\_QUERY\_GET\_CURRENT\_EVENT
set event to be the current TAU event.
C/C++:
TAU\_QUERY\_GET\_CURRENT\_EVENT
void \*
event
description
===========

``TAU_QUERY_GET_CURRENT_EVENT`` Set event to be the current TAU event in
the context in which this call is made.

example
=======

>\ **C/C++:**

::

    char[100] str;
    TAU_QUERY_DECLARE_EVENT(event);
    TAU_QUERY_GET_CURRENT_EVENT(event);
    TAU_QUERY_GET_EVENT_NAME(event, str);

    printf("current event is: %d.\n", str);

See Also
========

? ? ? ?

TAU\_QUERY\_GET\_EVENT\_NAME
TAU\_QUERY\_GET\_EVENT\_NAME
Gets the name of a given event.
C/C++:
TAU\_QUERY\_GET\_EVENT\_NAME
void \*
event
char \*
str
description
===========

``TAU_QUERY_GET_EVENT_NAME`` Set str to be the event name to the given
event name.

example
=======

>\ **C/C++:**

::

    char[100] str;
    TAU_QUERY_DECLARE_EVENT(event);
    TAU_QUERY_GET_CURRENT_EVENT(event);
    TAU_QUERY_GET_EVENT_NAME(event, str);

    printf("current event is: %d.\n", str);

See Also
========

? ? ? ?

TAU\_QUERY\_GET\_PARENT\_EVENT
TAU\_QUERY\_GET\_PARENT\_EVENT
gets the parent of the current event.
C/C++:
TAU\_QUERY\_GET\_PARENT\_EVENT
void \*
event
description
===========

``TAU_QUERY_GET_PARENT_EVENT`` Set event to be the parent event to the
current event.

example
=======

>\ **C/C++:**

::

    char[100] str;
    TAU_QUERY_DECLARE_EVENT(event);
    TAU_QUERY_GET_PARENT_EVENT(event);
    TAU_QUERY_GET_EVENT_NAME(event, str);

    printf("parent event is: %d.\n", str);

See Also
========

? ? ? ?
