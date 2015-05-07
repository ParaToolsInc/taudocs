KTAU Installation
=================

KTAU installation comprises 2 parts, kernel modification and user-API
library and utilities installation. KTAU distribution is organized as in
following hierarchy.

-  ktau/patches/ : Contains patches for various version of Linux kernel.

-  ktau/src/ : Contains extension to Linux kernel which is independent
   from version of the kernel.

-  ktau/usr-src/ : Contains user-space libraries and utilities.

-  ktau/misc/ : Contains works in progress.

Linux Kernel Modification
-------------------------

1. Obtain a distribution of KTAU from KTAU website.
   `(http://www.cs.uoregon.edu/research/ktau/downloads.php) <http://www.cs.uoregon.edu/research/ktau/downloads.php>`__

2. Obtain a distribution of Linux kernel from http://www.kernel.org.
   KTAU is ported to several versions of Linux. Please check in
   ``ktau/patches/`` directory for supported kernel versions

3. At ``ktau/src/linux-2.X/``, run

   ::

       sh INSTALL-kernel.sh <path to Linux kernel source> <patch name>

   This script will patch the kernel with the specified KTAU patch and
   install necessary files inside the kernel source tree.

4. At the root of Linux source tree, run ``make menuconfig`` and
   configure the kernel to enable KTAU. Save the configuration.

5. At the root of Linux source tree, run

   ::

       make clean dep bzImage modules moduels_install (for Linux-2.4)

   ::

       make clean bzImage modules modules_install     (for Linux-2.6)

   This will compile the kernel and install kernel. Then, configure
   system to boot with the new kernel, and reboot.

KTAU User-API Library and Utilities Installation
------------------------------------------------

1. At ``ktau/usr-src/src`` directory, run ``make clean all install``.
   The user-API library will be installed in ``ktau/lib/`` directory,
   and utilities will be installed in ``ktau/bin/`` directory.
