======
ResLnk
======
-------------
Resource Link
-------------

:Author: Jiang Yu-Kuan
:Contact: yukuan.jiang@gmail.com
:Revision: 0007
:Date: 2013-03-28

.. contents::


Introduction
============
The main goal of ResLnk (Resource Link) is to link resource files into single
one (link command). It provides map command to generate resource map file in C
array style, id command to generate a C header file of resource ID
enumeration. It also provids additional commmands (e.g. checksum, and
filesize) for the USB boot and the bootloading on A1016 ICs.


Usage
=====
Top level
---------
usage: reslnk.exe [-h] [-v] {link,map,id,checksum,filesize} ...

positional arguments:
  {link,map,id,checksum,filesize}
                        commands
    link                link resource files into single one.
    map                 generate a resource map file in format of C array.
    id                  generate a C header file of resource ID enumeration.
    checksum            generate a checksum header file for the USB boot on
                        A1016.
    filesize            generate a file-size header file (4-byte file-size in
                        a 256-byte header).

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit

link command
------------
usage: reslnk.exe link [-h] [-d <directory>] [-a <number>] [-p <char hex>]
                       [-o <file>]
                       lst-file

positional arguments:
  lst-file              The list file of resources.

optional arguments:
  -h, --help            show this help message and exit
  -d <directory>, --dir <directory>
                        assign the <directory> to read resource files. The
                        default directory is ".".
  -a <number>, --align <number>
                        specify the <number> of alignment bytes (default "1").
  -p <char hex>, --padding <char hex>
                        specify the padding hex value of a char (default
                        "0xFF").
  -o <file>, --output <file>
                        place the output into <file>, the file after linking
                        (default "res.bin").

map command
-----------
usage: reslnk.exe map [-h] [-d <directory>] [-a <number>] [-o <file>] lst-file

positional arguments:
  lst-file              The list file of resources.

optional arguments:
  -h, --help            show this help message and exit
  -d <directory>, --dir <directory>
                        assign the <directory> to read resource files. The
                        default directory is ".".
  -a <number>, --align <number>
                        specify the <number> of alignment bytes (default "1").
  -o <file>, --output <file>
                        place the output into <file>, the C included file
                        listing the offset, size pairs (default "ResMap.i").

id command
----------
usage: reslnk.exe id [-h] [-o <file>] lst-file

positional arguments:
  lst-file              The list file of resources.

optional arguments:
  -h, --help            show this help message and exit
  -o <file>, --output <file>
                        place the output into <file>, the C header file of
                        resource ID enumeration (default "ResID.h").

checksum command
----------------
usage: reslnk.exe checksum [-h] [-o <file>] binary-file

positional arguments:
  binary-file           The firmware binary file used to calculate checksum
                        and filesize fields of the USB ISP header

optional arguments:
  -h, --help            show this help message and exit
  -o <file>, --output <file>
                        place the output into <file>, the checksum header file
                        (default "checksum.bin").

filesize command
----------------
usage: reslnk.exe filesize [-h] [-o <file>] binary-file

positional arguments:
  binary-file           The firmware binary file used to calculate file-size

optional arguments:
  -h, --help            show this help message and exit
  -o <file>, --output <file>
                        place the output into <file>, the file-size header
                        file (default "filesize.bin").

ToDo List
=========


Version History
===============
0.99
----
Released 2013-03-28

* Added align option to map and link commands for specifying the number of
  alignment bytes.


0.12
----
Released 2013-03-22

* Added usb_head command to generate USB ISP header file of A1016
* Renamed usb_head command to checksum command
* Added padding option to link command
* Added filesize command to generate a filesize header file
* Appended newline on generated resource map files (e.g. ResMap.i)

0.02
----
Released 2013-2-27

* Initial version
* Added commands of link, map, and id

