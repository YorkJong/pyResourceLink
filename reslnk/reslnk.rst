======
ResLnk
======
-------------
Resource Link
-------------

:Author: Jiang Yu-Kuan
:Contact: yukuan.jiang@gmail.com
:Revision: 0004
:Date: 2013-03-13

.. contents::


Introduction
============
The main goal of ResLnk (Resource Link) is to link resource files into single
one (link command).  It also provids map command to generate resource map file
in C array style, and id command to generate a C header file of resource ID
enumeration.

Usage
=====
Top level
---------
positional arguments:
  {link,map,id,checksum}
                        commands
    link                link resource files into single one.
    map                 generate a resource map file in format of C array.
    id                  generate a C header file of resource ID enumeration.
    checksum            generate a checksum header file for the USB ISP of
                        A1016.

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit

link command
------------
usage: reslnk.exe link [-h] [-d <directory>] [-p <char hex>] [-o <file>]
                       lst-file

positional arguments:
  lst-file              The list file of resources.

optional arguments:
  -h, --help            show this help message and exit
  -d <directory>, --dir <directory>
                        assign the <directory> to read resource files. The
                        default directory is ".".
  -p <char hex>, --padding <char hex>
                        specify the padding hex value of a char (default
                        "0xFF").
  -o <file>, --output <file>
                        place the output into <file>, the file after linking
                        (default "res.bin").

map command
-----------
usage: reslnk.exe map [-h] [-d <directory>] [-o <file>] lst-file

positional arguments:
  lst-file              The list file of resources.

optional arguments:
  -h, --help            show this help message and exit
  -d <directory>, --dir <directory>
                        assign the <directory> to read resource files. The
                        default directory is ".".
  -o <file>, --output <file>
                        place the output into <file>, the C included file
                        listing the offset, size pairs (default "res_map.i").

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

ToDo List
=========


Version History
===============
0.10
----
Released 2013-03-13

* Added usb_head command to generate USB ISP header file of A1016
* Renamed usb_head command to checksum command
* Added padding option to link command

0.02
----
Released 2013-2-27

* Initial version
* Added commands of link, map, and id

