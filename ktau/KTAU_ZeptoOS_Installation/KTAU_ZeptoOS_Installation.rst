KTAU Installation for ANL BlueGene/L System
===========================================

KTAUD and KTAU Utilities Installation
-------------------------------------

1. Obtain a distribution of KTAU from KTAU website.
   (`http://www.cs.uoregon.edu/research/ktau/download.php <http://www.cs.uoregon.edu/research/ktau/downloads.php>`__)

2. At ``ZeptoOS/BGL`` dirctory, run ``configure --edit.`` This will
   launch the ZeptoOS configuration tool. Select on KTAUD parameters,
   enable KTAUD, and configure the parameters. Please refer to the help
   section of each configuration for more detail.

3. Save configuration, and run ``make clean all install``. At this
   point, `` ktaud, ktaud.conf
           and ktaud.sh `` should be configured and installed in the
   ZeptoOS build directory (``/ZeptoOS/BGL/build/ZeptoOS-<version>``).
   The installation also includes ``ktaud.sh`` in the ramdisk image.

4. At ``ZeptoOS/BGL/ionode-ramdisk`` directory, run
   ``make clean all install`` to recreate the ramdisk image which will
   include ktaud.sh in ``ZeptoOS/BGL/ionode-ramdisk/datatree/etc/rc.d/``

5. To change the KTAUD configuration later on, simply run
   ``configure --edit`` at ``ZeptoOS/BGL/`` directory, and run
   ``make clean all install``. In this case, there is no need to rebuild
   the ramdisk image unless the path to the ``ktaud`` and ``ktaud.conf``
   are changed.

KTAU Installation
-----------------

1. At ``ZeptoOS/BGL/ionode-linux-2.4.19/`` directory, run
   ``make .config`` to uncompress the Linux kernel source, patch the
   vanilla kernel with BGL patches, and configure the kernel.

2. At ``ktau/src/linux-2.4/``, run

   ::

       sh INSTALL-kernel.sh <path to ZeptoOS>/BGL/ionode-linux-2.4.19/linux-2.4.19 patch-2.4.19-ZeptoOS-1.1_ktau-1.6

   This script willl patch the kernel with KTAU patch and install
   necessary files inside the kernel source tree.

3. At ``ZeptoOS/BGL/ionode-linux-2.4.19/linux-2.4.19/`` directory, run
   ``make menuconfig`` and configure the kernel to enable KTAU. Save the
   configuration.

4. At ``ZeptoOS/BGL/ionod-linux-2.4.19`` directory, run
   ``rm zImage.elf``, and then run ``make clean all install``. This will
   compile the kernel and install the kernel image (zImage.elf) in the
   ZeptoOS build directory.
