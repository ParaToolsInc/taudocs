TAU allows the user to map performance data of entities from one layer
to another in multi-layered software. Mapping is used in profiling (and
tracing) both synchronous and asynchronous models of computation.

For mapping, the following macros are used. First locate and identify
the higher-level statement using the ? macro. Then, associate a function
identifier with it using the ?. Associate the high level statement to a
FunctionInfo object that will be visible to lower level code, using ?,
and then profile entire blocks using ?. Independent sets of statements
can be profiled using ?, ?, and ? macros using the FunctionInfo object.

The TAU ``examples/mapping`` directory has two examples (embedded and
external) that illustrate the use of this mapping API for generating
object-oriented profiles.

TAU\_MAPPING
3
TAU\_MAPPING
Encapsulates a C++ statement for profiling
C/C++:
TAU\_MAPPING
statement
statement
TauGroup\_t
key
Description
===========

``TAU_MAPPING`` is used to encapsulate a C++ statement as a timer. A
timer will be made, named by the statment, and will profile the
statement. The key given can be used with ? to retrieve the timer.

Example
=======

**C/C++ :**

::

    int main(int argc, char **argv) {
      Array <2> A(N, N), B(N, N), C(N,N), D(N, N);
      // Original statement:
      // A = B + C + D;
      //Instrumented statement:
      TAU_MAPPING(A = B + C + D; , TAU_USER);
      ... 
    }
        

See Also
========

?, ?

TAU\_MAPPING\_CREATE
3
TAU\_MAPPING\_CREATE
Creates a mapping
C/C++:
TAU\_MAPPING\_CREATE
char \*
name
char \*
type
char \*
groupname
unsigned long
key
int
tid
Description
===========

``TAU_MAPPING_CREATE`` creates a mapping and associates it with the key
that is specified. Later, this key may be used to retrieve the
FunctionInfo object associated with this key for timing purposes. The
thread identifier is specified in the ``tid`` parameter.

Example
=======

**C/C++ :**

::

    class MyClass {
      public:
        MyClass() {
          TAU_MAPPING_LINK(runtimer, TAU_USER); 
        } 
        ~MyClass() {}

        void Run(void) {
          TAU_MAPPING_PROFILE(runtimer); // For one object
          TAU_PROFILE("MyClass::Run()", " void (void)", TAU_USER1);
        
          cout <<"Sleeping for 2 secs..."<<endl;
          sleep(2);
        }
      private:
        TAU_MAPPING_OBJECT(runtimer)  // EMBEDDED ASSOCIATION
    };

    int main(int argc, char **argv) {
      TAU_PROFILE_INIT(argc, argv);
      TAU_PROFILE("main()", "int (int, char **)", TAU_DEFAULT);
      MyClass x, y, z;
      TAU_MAPPING_CREATE("MyClass::Run() for object a", " " , TAU_USER, 
                         "TAU_USER", 0);
      MyClass a;
      TAU_PROFILE_SET_NODE(0);
      cout <<"Inside main"<<endl;

      a.Run();
      x.Run();
      y.Run();
    }
        

See Also
========

?, ?, ?

TAU\_MAPPING\_LINK
3
TAU\_MAPPING\_LINK
Creates a mapping link
C/C++:
TAU\_MAPPING\_LINK
FunctionInfo
FuncIdVar
unsigned long
Key
Description
===========

``TAU_MAPPING_LINK ``\ creates a link between the object defined in
``TAU_MAPPING_OBJECT`` (that identifies a statement) and the actual
higher-level statement that is mapped with ``TAU_MAPPING``. The Key
argument represents a profile group to which the statement belongs, as
specified in the ``TAU_MAPPING`` macro argument. For the example of
array statements, this link should be created in the constructor of the
class that represents the expression. ``TAU_MAPPING_LINK`` should be
executed before any measurement takes place. It assigns the identifier
of the statement to the object to which FuncIdVar refers. For example

Example
=======

**C/C++ :**

::

    class MyClass {
      public:
        MyClass() { }
        ~MyClass() { }

        void Run(void) {
          TAU_MAPPING_OBJECT(runtimer)
          TAU_MAPPING_LINK(runtimer, (unsigned long) this);
          TAU_MAPPING_PROFILE(runtimer); // For one object
          TAU_PROFILE("MyClass::Run()", " void (void)", TAU_USER1);
          
          /* ... */
        }
    };

    int main(int argc, char **argv) {
      TAU_PROFILE_INIT(argc, argv);
      TAU_PROFILE("main()", "int (int, char **)", TAU_DEFAULT);
      MyClass x, y, z;
      MyClass a;
      TAU_MAPPING_CREATE("MyClass::Run() for object a", " " , 
                         (TauGroup_t) &a, "TAU_USER", 0);
      TAU_MAPPING_CREATE("MyClass::Run() for object x", " " , 
                         (TauGroup_t) &x, "TAU_USER", 0);
      TAU_PROFILE_SET_NODE(0);
      cout <<"Inside main"<<endl;

      a.Run();
      x.Run();
      y.Run();


        

See Also
========

?, ?, ?

TAU\_MAPPING\_OBJECT
3
TAU\_MAPPING\_OBJECT
Declares a mapping object
C/C++:
TAU\_MAPPING\_OBJECT
FunctionInfo
FuncIdVar
Description
===========

To create storage for an identifier associated with a higher level
statement that is mapped using ``TAU_MAPPING``, we use the
``TAU_MAPPING_OBJECT`` macro. For example, in the ``TAU_MAPPING``
example, the array expressions are created into objects of a class
ExpressionKernel, and each statement is an object that is an instance of
this class. To embed the identity of the statement we store the mapping
object in a data field in this class. This is shown below:

Example
=======

**C/C++ :**

::

    template<class LHS,class Op,class RHS,class EvalTag>
    class ExpressionKernel : public Pooma::Iterate_t {
      public:
          
        typedef ExpressionKernel<LHS,Op,RHS,EvalTag> This_t;
        //
        // Construct from an Expr.
        // Build the kernel that will evaluate the expression on the 
        // given domain.
        // Acquire locks on the data referred to by the expression.
        //
        ExpressionKernel(const LHS&,const Op&,const RHS&,
        Pooma::Scheduler_t&);
          
          
        virtual ~ExpressionKernel();
        
        // Do the loop.
        virtual void run();
        
      private:
          
        // The expression we will evaluate.
        LHS lhs_m;
        Op  op_m;
        RHS rhs_m;
        TAU_MAPPING_OBJECT(TauMapFI)
    };
        

See Also
========

?, ?, ?

TAU\_MAPPING\_PROFILE
3
TAU\_MAPPING\_PROFILE
Profiles a block based on a mapping
C/C++:
TAU\_MAPPING\_PROFILE
FunctionInfo \*
FuncIdVar
Description
===========

The ``TAU_MAPPING_PROFILE`` macro measures the time and attributes it to
the statement mapped in ``TAU_MAPPING`` macro. It takes as its argument
the identifier of the higher level statement that is stored using
``TAU_MAPPING_OBJECT`` and linked to the statement using
``TAU_MAPPING_LINK`` macros. ``TAU_MAPPING_PROFILE`` measures the time
spent in the entire block in which it is invoked. For example, if the
time spent in the run method of the class does work that must be
associated with the higher-level array expression, then, we can
instrument it as follows:

Example
=======

**C/C++ :**

::

    // Evaluate the kernel
    // Just tell an InlineEvaluator to do it.
          
    template<class LHS,class Op,class RHS,class EvalTag>
    void
    ExpressionKernel<LHS,Op,RHS,EvalTag>::run() {
      TAU_MAPPING_PROFILE(TauMapFI)
          
      // Just evaluate the expression.
      KernelEvaluator<EvalTag>().evalate(lhs_m,op_m,rhs_m);
      // we could release the locks here or in dtor 
    }
        

See Also
========

?, ?, ?

TAU\_MAPPING\_PROFILE\_START
3
TAU\_MAPPING\_PROFILE\_START
Starts a mapping timer
C/C++:
TAU\_MAPPING\_PROFILE\_START
Profiler
timer
int
tid
Description
===========

``TAU_MAPPING_PROFILE_START`` starts the timer that is created using
``TAU_MAPPING_PROFILE_TIMER``. This will measure the elapsed time in
groups of statements, instead of the entire block. A corresponding stop
statement stops the timer as described next. The thread identifier is
specified in the tid parameter.

Example
=======

**C/C++ :**

::

    template<class LHS,class Op,class RHS,class EvalTag>
    void
    ExpressionKernel<LHS,Op,RHS,EvalTag>::run() {
      TAU_MAPPING_PROFILE_TIMER(timer, TauMapFI);
      printf("ExpressionKernel::run() this = 4854\n", this);
      // Just evaluate the expression.
      
      TAU_MAPPING_PROFILE_START(timer);
      KernelEvaluator<EvalTag>().evaluate(lhs_m, op_m, rhs_m);
      TAU_MAPPING_PROFILE_STOP();
      // we could release the locks here instead of in the dtor.
    }
        

See Also
========

?, ?

TAU\_MAPPING\_PROFILE\_STOP
3
TAU\_MAPPING\_PROFILE\_STOP
Stops a mapping timer
C/C++:
TAU\_MAPPING\_PROFILE\_STOP
Profiler
timer
int
tid
Description
===========

``TAU_MAPPING_PROFILE_STOP`` stops the timer that is created using
``TAU_MAPPING_PROFILE_TIMER``. This will measure the elapsed time in
groups of statements, instead of the entire block. A corresponding stop
statement stops the timer as described next. The thread identifier is
specified in the tid parameter.

Example
=======

**C/C++ :**

::

    template<class LHS,class Op,class RHS,class EvalTag>
    void
    ExpressionKernel<LHS,Op,RHS,EvalTag>::run() {
      TAU_MAPPING_PROFILE_TIMER(timer, TauMapFI);
      printf("ExpressionKernel::run() this = 4854\n", this);
      // Just evaluate the expression.
      
      TAU_MAPPING_PROFILE_START(timer);
      KernelEvaluator<EvalTag>().evaluate(lhs_m, op_m, rhs_m);
      TAU_MAPPING_PROFILE_STOP();
      // we could release the locks here instead of in the dtor.
    }
        

See Also
========

?, ?

TAU\_MAPPING\_PROFILE\_TIMER
3
TAU\_MAPPING\_PROFILE\_TIMER
Declares a mapping timer
C/C++:
TAU\_MAPPING\_PROFILE\_TIMER
Profiler
timer
FunctionInfo \*
FuncIdVar
Description
===========

``TAU_MAPPING_PROFILE_TIMER`` enables timing of individual statements,
instead of complete blocks. It will attribute the time to a higher-level
statement. The second argument is the identifier of the statement that
is obtained after ``TAU_MAPPING_OBJECT`` and ``TAU_MAPPING_LINK`` have
executed. The timer argument in this macro is any variable that is used
subsequently to start and stop the timer.

Example
=======

**C/C++ :**

::

    template<class LHS,class Op,class RHS,class EvalTag>
    void
    ExpressionKernel<LHS,Op,RHS,EvalTag>::run() {
      TAU_MAPPING_PROFILE_TIMER(timer, TauMapFI);
      printf("ExpressionKernel::run() this = 4854\n", this);
      // Just evaluate the expression.
      
      TAU_MAPPING_PROFILE_START(timer);
      KernelEvaluator<EvalTag>().evaluate(lhs_m, op_m, rhs_m);
      TAU_MAPPING_PROFILE_STOP();
      // we could release the locks here instead of in the dtor.
    }
        

See Also
========

?, ?, ?, ?
