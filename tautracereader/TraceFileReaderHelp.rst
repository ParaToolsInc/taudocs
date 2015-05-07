TAU Trace Format Reader Library
===============================

Tau Reader Usage
----------------

SYNOPSIS
~~~~~~~~

An API for reading data from TAU tracefiles

See TAU\_tf.h

DESCRIPTION
~~~~~~~~~~~

The TAU Trace Format Reader system, defined in TAU\_tf.h, operates
primarily via a series C/C++ of callback methods, each representing a
data type contained in a TAU tracefile. The TAU trace is opened with a
call to the function: Ttf\_FileHandleT Ttf\_OpenFileForInput( const char
\*name, const char \*edf); Where \*name and \*edf are the locations of
the TAU trace and event definition files to be read respectively. The
TtfFileHandleT returned is then used to access the TAU trace. e.g: fh =
Ttf\_OpenFileForInput( argv[1], argv[2]);

The callback methods are stored in a callback table, a struct of the
type Ttf\_Callbacks. The Ttf\_Callbacks struct contains entities
representing each of the 11 defined callbacks: Ttf\_DefClkPeriodT
DefClkPeriod; Ttf\_DefThreadT DefThread; Ttf\_DefStateGroupT
DefStateGroup; Ttf\_DefStateT DefState; Ttf\_EndTraceT EndTrace;
Ttf\_EnterStateT EnterState; Ttf\_LeaveStateT LeaveState;
Ttf\_SendMessageT SendMessage; Ttf\_RecvMessageT RecvMessage;
Ttf\_DefUserEvent DefUserEvent; Ttf\_EventTrigger EventTrigger; The
struct also contains "void\* UserData;" which is used as an argument to
each of the callback functions.

The trace data relevant to a callback function's associated TAU event
type are delivered to the function via its arguments. Additionally the
user data argument may be used to pass in data defined elsewhere in the
trace reading process, before the callback functions are invoked. The
userData argument is often used to provide the file handler for
functions to which the read trace events are being written. The userData
argument must be recast to its original type before use. For example,
the following callback function, compliant with the definition of
Ttf\_DefClkPeriodT, receives the clock period information from the TAU
tracefile, in addition to the userData that specifies the the location
of sprintf's target.

::

    int ClockPeriod (void* userData, double clkPeriod ) {
        sprintf((char*)userData,"Clock period %g\n", clkPeriod);
        return 0;
    }

The callback table should be initialized by associating each of its
elements with a complementary callback function. As the trace file is
read the contents of each entry will be passed to the corresponding
callback function. Alternatively if an element of the callback table is
set to 0 no action will be taken when its associated entry type is
encountered. Each element of the callback table must be initialized to a
viable function or 0. For example, to create a callback table, tb, and
initialize the DefClkPeriod element with the function defined above one
would use the following:

::

    Ttf_CallbacksT cb;
    cb.DefClkPeriod = ClockPeriod;

Once the callback table is initialized the tracefile reading may
commence. This is done via the Ttf\_ReadNumEvents function defined in
TAU\_tf.h. Because Ttf\_ReadNumEvents requires trace files to be read in
chunks of events of the number specified when the function is called it
is common practice to read a tracefile by enclosing TtfReadNumEvents in
a loop which terminates when there are no records left to read (i.e. the
return value of TtF\_ReadNumEvents is 0). The EndTrace callback function
may also set a flag that breaks out of the loop. For example, using the
Ttf\_FileHandleT fh and Ttf\_CallbacksT cb the following would process
the entire tracefile specified within fh:

::

    do{
        recs_read = Ttf_ReadNumEvents(fh,cb, 1024);
    }
    while (recs_read >=0);

In some circumstances it may be convenient to parse the trace files more
than once using different callback tables and methods. For example, this
technique is often useful when all of the the initialization records
must be registered and processed before the event records.

When the processing of a tracefile is complete the tracefile should be
closed with the Ttf\_CloseFile( Ttf\_FileHandleT fileHandle ); function.
eg:

::

    Ttf_CloseFile(fh);

Callback API
------------

int Ttf\_DefClkPeriodT(userData, clkPeriod );
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``
Arguments: void* userData, double clkPeriod
``

``
Returns: int status
``

This method is called when the trace reader encounters the definition of
the clock period of the trace being read. It is called with the user
defined argument userData and the clock period, clkPeriod, defined in
the TAU trace. It should return 0 upon successful completion.

int Ttf\_EndTraceT(userData,nodeToken,threadToken);
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``
Arguments: void *userData, unsigned int nodeToken, unsigned int threadToken
``

``
Returns: int status
``

This method is called when an EOF is encountered in a tracefile. It is
called with the user defined argument userData and the numeric ID of the
node and thread, nodeToken and threadToken respectively, where the trace
has ended. Note that the full trace has not concluded until the end of
each node/thread combination has been reached. It should return 0 upon
successful completion.

int Ttf\_DefStateGroupT(userData, stateGroupToken, stateGroupName );
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``
Arguments: void *userData, unsigned int stateGroupToken, const char *stateGroupName
``

``
Returns: int status
``

This method is called when the trace reader encounters a state group
definition. It is called with the user defined argument userData the
numeric ID of the state group being defined, stateGroupToken, and the
name of the group being defined, stateGroupName. It should return 0 upon
successful completion.

int Ttf\_DefStateT(userData, stateToken, stateName, stateGroupToken );
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``
Arguments: void *userData, unsigned int stateToken, const char *stateName, unsigned int stateGroupToken
``

``
Returns: int status
``

This method is called when the trace reader encounters a state
definition. A state generally represents a programmatic function. It is
called with the user defined argument userData, the numeric ID of the
state being defined, stateToken, the name of the state being defined,
stateName, and the numeric group ID of the state being defined,
stateGroupToken. It should return 0 upon successful completion.

int Ttf\_DefUserEvent(userData, userEventToken, userEventName, monotonicallyIncreasing);
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``
Arguments: void *userData, unsigned int userEventToken, const char *userEventName, int monotonicallyIncreasing
``

``
Returns: int status
``

This method is called when the trace reader encounters a user defined
event definition. It is called with the user defined argument userData,
the numeric ID of the user defined event, userEventToken, the name of
the user defined event, userEventName, and monotonicallyIncreasing a
numeric indicator of if the user defined event is monotonically
Increasing. If monotonicallyIncreasing is greater than 0 the user
defined event's value will increase monotonically. If it is 0 then it
will not be. It should return 0 upon successful completion.

int Ttf\_EnterStateT(userData, time, nodeToken, threadToken, stateToken );
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``
Arguments: void*  userData, double time, unsigned int nodeToken, unsigned int threadToken, unsigned int stateToken
``

``
Returns: int status
``

This method is called when the trace reader encounters a state entry
event. It is called with the user defined argument userData, the time of
the state entry, time, the numeric ID of the node and thread where the
entry is taking place, nodeToken and threadToken respectively, and the
numeric ID of the state that has been entered. It should return 0 upon
successful completion.

int Ttf\_LeaveStateT(userData, time, nodeToken, threadToken );
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``
Arguments: void*  userData, double time, unsigned int nodeToken, unsigned int threadToken
``

``
Returns: int status
``

This method is called when the trace reader encounters a state exit
event. It is called with the user defined argument userData, the time of
the state exit, time and the numeric IDs of the node and thread where
the exit is taking place, nodeToken and threadToken respectively. It
should return 0 upon successful completion.

int Ttf\_SendMessageT(userData, time, sourceNodeToken, sourceThreadToken, destinationNodeToken, destinationThreadToken, messageSize, int messageTag);
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``
Arguments: void*  userData, double time, unsigned int sourceNodeToken, unsigned int sourceThreadToken, unsigned int destinationNodeToken, unsigned int destinationThreadToken, unsigned int messageSize, unsigned int messageTag
``

``
Returns: int status
``

This method is called when the trace reader encounters a message send
event. It is called with the user defined argument userData, the time of
the transmission, time, the numeric IDs of the node and thread from
which the message was sent, sourceNodeToken and sourceThreadToken
respectively, the numeric IDs of the node and thread to which the
message was sent, destinationNodeToken and destinationThreadToken
respectively, the size of the message, messageSize, and the numeric ID
of the message, messageTag. It should return 0 upon successful
completion.

int Ttf\_RecvMessageT(userData, time, sourceNodeToken, sourceThreadToken, destinationNodeToken, destinationThreadToken, messageSize, int messageTag);
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``
Arguments: void*  userData, double time, unsigned int sourceNodeToken, unsigned int sourceThreadToken, unsigned int destinationNodeToken, unsigned int destinationThreadToken, unsigned int messageSize, unsigned int messageTag
``

``
Returns: int status
``

This method is called when the trace reader encounters a message receive
event. It is called with the user defined argument userData, the time of
the receipt, time, the numeric IDs of the node and thread from which the
message was sent, sourceNodeToken and sourceThreadToken respectively,
the numeric IDs of the node and thread to which the message was sent,
destinationNodeToken and destinationThreadToken respectively, the size
of the message, messageSize, and the numeric ID of the message,
messageTag. It should return 0 upon successful completion.

int Ttf\_EventTrigger(userData, time, nodeToken, threadToken, userEventToken, userEventValue);
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``
Arguments: void *userData, double time, unsigned int nodeToken, unsigned int threadToken, unsigned int userEventToken, long long userEventValue
``

``
Returns: int status
``

This method is called when the trace reader encounters a user defined
event trigger. It is called with the user defined argument data
userData, the time of the event trigger, time, the numeric IDs of the
node and thread where the event was triggered, nodeToken and threadToken
respectively, the numeric ID of the user defined event triggered,
userEventToken and the value recorded by the user defined event,
userEventValue. It should return 0 upon successful completion.

TauReader API
-------------

Ttf\_FileHandleT TtfOpenFileForInput(name, edf);
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``
Arguments: const char *name, const char *edf
``

``
Returns: Ttf_FileHandleT fileHandle
``

Given the full name of the TAU trace file, name, and the corresponding
event file, edf, and returns the virtual file handle that represents the
trace in its entirety.

int Ttf\_AbsSeek(handle, eventPosition);
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``
Arguments: Ttf_FileHandleT handle, int eventPosition
``

``
Returns: int position
``

Given a Ttf\_fileHandleT object, handle, this function will move to the
nth event in the associated tracefile where n = the input int
eventPosition. A negative position indicates to start from the tail of
the event stream. The position will be returned if the operation is
successful, otherwise it will return 0.

int Ttf\_RelSeek(handle, plusMinusNumEvents);
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``
Arguments: Ttf_FileHandleT handle, int plusMinusNumEvents
``

``
Returns: int position
``

Given a Ttf\_fileHandleT object, handle, this function will shift the
current position by a number of events equal to the input int
plusMinusNumEvents. The new position will be returned if the operation
is successful, otherwise it will return 0.

int Ttf\_ReadNumEvents(fileHandle,callbacks, numberOfEvents);
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``
Arguments: Ttf_FileHandleT fileHandle, Ttf_CallbacksT callbacks, int numberOfEvents
``

``
Returns: int numEventsRead
``

Given a Ttf\_FileHandleT, handle, a fully initialized Ttf\_CallbacksT
struct, callbacks, and an integer indicating the number of events to
read, numberOfEvents, this function will read the number of events
indicated starting at the current position of the file handle while
advancing the current position of the handle by that number. Each event
read will be sent to the appropriate callback function specified in the
callbacks. When successful this function returns the number of events
read. This may be 0 or less than the number specified if there are fewer
remaining events to be read than numberOfEvents requests. If an error is
encountered it will return -1.

Ttf\_FileHandleT Ttf\_CloseFile(fileHandle);
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``
Arguments: Ttf_FileHandleT fileHandle
``

``
Returns: Ttf_FileHandleT fileHandle
``

When the tracefile reading is complete the file should be closed with
this function.
