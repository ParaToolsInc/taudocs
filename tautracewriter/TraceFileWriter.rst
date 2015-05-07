TAU Trace Format Writer Library
===============================

Tau Writer Usage
----------------

SYNOPSIS
~~~~~~~~

An API for writing TAU trace files

See TAU\_tf.h

DESCRIPTION
~~~~~~~~~~~

The TAU Trace Format Writer system, defined in TAU\_tf.h, operates as a
series of function calls that define the TAU trace file format. A TAU
trace file is started with a call to the function:

::

    Ttf_FileHandleT Ttf_OpenFileForOutput( const char *name, const char *edf)

Where \*name and \*edf are the locations of the TAU trace and event
definition files to be written respectively. The TtfFileHandleT returned
is then used to write the rest of the TAU trace. e.g: fh =
Ttf\_OpenFileForInput( argv[1], argv[2]);

TAU Trace File Writer API
-------------------------

int Ttf\_DefClkPeriodT(Ttf\_FileHandleT file, double clkPeriod );
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``
    Arguments: Ttf_FileHandleT file, double clkPeriod
      ``

``
      Returns: int status
    ``

This method is called to define the clock period of the trace being
written. It should return 0 upon successful completion.

int Ttf\_EndTraceT(Ttf\_FileHandleT file, nodeToken, threadToken);
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``
      Arguments: Ttf_FileHandleT file, unsigned int nodeToken, unsigned int threadToken
    ``

``
    Returns: int status
      ``

This method is called to mark an "End of Trace" event for a particular
node/thread pair. It should return 0 upon successful completion.

int Ttf\_DefStateGroupT(Ttf\_FileHandleT file, stateGroupToken, stateGroupName );
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``
      Arguments: Ttf_FileHandleT file, unsigned int stateGroupToken, const char *stateGroupName
      ``

``
    Returns: int status
      ``

This method is called to define a state group. It is called with the
trace file handler and the numeric ID of the state group being defined,
stateGroupToken, and the name of the group being defined,
stateGroupName. It should return 0 upon successful completion.

int Ttf\_DefStateT(Ttf\_FileHandleT file, stateToken, stateName, stateGroupToken );
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``
    Arguments: Ttf_FileHandleT file, unsigned int stateToken, const char
    *stateName, unsigned int stateGroupToken
      ``

``
    Returns: int status
      ``

This method is called to write a state definition. A state generally
represents a programmatic function. It should return 0 upon successful
completion.

int Ttf\_DefUserEvent(Ttf\_FileHandleT file, userEventToken, userEventName, monotonicallyIncreasing);
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``
    Arguments: Ttf_FileHandleT file, unsigned int userEventToken, const char
    *userEventName, int monotonicallyIncreasing
      ``

``
    Returns: int status
      ``

This method is called when writing a user defined event definition. It
should return 0 upon successful completion.

int Ttf\_EnterStateT(Ttf\_FileHandleT file, time, nodeToken, threadToken, stateToken );
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``
    Arguments: Ttf_FileHandleT file, double time, unsigned int nodeToken,
    unsigned int threadToken, unsigned int stateToken
      ``

``Returns: int status
      ``

This method is called to write a state entry event. It is called with
the trace file handler, the time of the state entry, time, the numeric
ID of the node and thread where the entry is taking place, nodeToken and
threadToken respectively, and the numeric ID of the state that has been
entered. It should return 0 upon successful completion.

int Ttf\_LeaveStateT(Ttf\_FileHandleT file, time, nodeToken, threadToken );
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``
    Arguments: Ttf_FileHandleT file, double time, unsigned int nodeToken,
    unsigned int threadToken
      ``

``
    Returns: int status
      ``

This method is called to finish writing to a state. It is called with
the trace file handler, the time of the state exit, time and the numeric
IDs of the node and thread where the exit is taking place, nodeToken and
threadToken respectively. It should return 0 upon successful completion.

int Ttf\_SendMessageT(Ttf\_FileHandleT file, time, sourceNodeToken, sourceThreadToken, destinationNodeToken, destinationThreadToken, messageSize, int messageTag);
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``
    Arguments: Ttf_FileHandleT file, double time, unsigned int sourceNodeToken,
    unsigned int sourceThreadToken, unsigned int destinationNodeToken,
    unsigned int destinationThreadToken, unsigned int messageSize, unsigned
    int messageTag
      ``

``
    Returns: int status``

This method is called write a message send event. It is called with the
trace file handler, the time of the transmission, time, the numeric IDs
of the node and thread from which the message was sent, sourceNodeToken
and sourceThreadToken respectively, the numeric IDs of the node and
thread to which the message was sent, destinationNodeToken and
destinationThreadToken respectively, the size of the message,
messageSize, and the numeric ID of the message, messageTag. It should
return 0 upon successful completion.

int Ttf\_RecvMessageT(Ttf\_FileHandleT file, time, sourceNodeToken, sourceThreadToken, destinationNodeToken, destinationThreadToken, messageSize, int messageTag);
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``
    Arguments: Ttf_FileHandleT file, double time, unsigned int sourceNodeToken,
    unsigned int sourceThreadToken, unsigned int destinationNodeToken,
    unsigned int destinationThreadToken, unsigned int messageSize, unsigned
    int messageTag
      ``

``
    Returns: int status
      ``

This method is called to write a message receive event. It is called
with the trace file handler, the time of the receipt, time, the numeric
IDs of the node and thread from which the message was sent,
sourceNodeToken and sourceThreadToken respectively, the numeric IDs of
the node and thread to which the message was sent, destinationNodeToken
and destinationThreadToken respectively, the size of the message,
messageSize, and the numeric ID of the message, messageTag. It should
return 0 upon successful completion.

int Ttf\_EventTrigger(Ttf\_FileHandleT file, time, nodeToken, threadToken, userEventToken, userEventValue);
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``
      Arguments: Ttf_FileHandleT file, double time, unsigned int nodeToken,
      unsigned int threadToken, unsigned int userEventToken, long long
      userEventValue
    ``

``
      Returns: int status
    ``

This method is called to write a user defined event trigger. It is
called with the trace file handler, the time of the event trigger, time,
the numeric IDs of the node and thread where the event was triggered,
nodeToken and threadToken respectively, the numeric ID of the user
defined event triggered, userEventToken and the value recorded by the
user defined event, userEventValue. It should return 0 upon successful
completion.

TauReader API
-------------

Ttf\_FileHandleT TtfOpenFileForOutput(name, edf);
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``
    Arguments: const char *name, const char *edf
      ``

``
    Returns: Ttf_FileHandleT fileHandle
      ``

Given the full name of the TAU trace file, name, and the corresponding
event file, edf, and returns a handle for the trace to be used with
other trace writing functions.

int Ttf\_AbsSeek(handle, eventPosition);
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``
    Arguments: Ttf_FileHandleT handle, int eventPosition
      ``

``
    Returns: int position
      ``
