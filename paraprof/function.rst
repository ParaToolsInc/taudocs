Function Based Displays
=======================

ParaProf has two displays for showing a single function across all
threads of execution. This chapter describes the Function Bar Graph
Window and the Function Histogram Window.

Function Bar Graph
==================

|Function Bar Graph|

This display graphs the values that the particular function had for each
thread along with the mean and standard deviation across the threads.
You may also change the units and metric displayed from the *Options*
menu.

Function Histogram
==================

|Function Histogram|

This display shows a histogram of each thread's value for the given
function. Hover the mouse over a given bar to see the range minimum and
maximum and how many threads fell into that range. You may also change
the units and metric displayed from the *Options* menu.

You may also dynamically change how many bins are used (1-100) in the
histogram. This option is available from the *Options* menu. Changing
the number of bins can dramatically change the shape of the histogram,
play around with it to get a feel for the true distribution of the data.

.. |Function Bar Graph| image:: functionbargraph.gif
.. |Function Histogram| image:: functionhistogram.gif
