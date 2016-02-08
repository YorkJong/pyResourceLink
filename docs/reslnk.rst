======
ResLnk
======
-------------
Resource Link
-------------

:Author: Jiang Yu-Kuan
:Contact: yukuan.jiang@gmail.com
:Revision: 0018
:Date: 2016-02-08

.. contents::


Introduction
============
The main goal of ResLnk (Resource Link) is to link resource files into single
one (*link* command). It provides also *map* command to generate a resource
map file in C array style, *bmap* command to generate the resource map file in
binary style, and *id* command to generate a C header file of resource ID
enumeration.


Usage
=====
Top level
---------
usage: reslnk.exe [-h] [-v] {link,map,bmap,id} ...

positional arguments:
  {link,map,bmap,id}
                        commands
    link                link resource files into single one.
    map                 generate a resource map file in format of C array.
    bmap                generate a resource map file in binary format.
    id                  generate a C header file of resource ID enumeration.

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

bmap command
------------
usage: reslnk.exe bmap [-h] [-d <directory>] [-a <number>] [-o <file>] lst-file

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
                        place the output into <file>, the binary version of
                        resource map file listing the offset, size pairs
                        (default "ResMap.bin").

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

ToDo List
=========


Version History
===============
1.14
----
Released 2016-02-08

- Extracted myutil.py from reslnk.py
- Added README.md
- Added CHANGELOG.md
- Added LICENSE.md
- Hosted to bitbucket.org
- Moved files for distribute.bat
- Removed filesize command
- Removed checksum command

1.13
----
Released 2015-04-07

- Added allowing for *empty kinds* in generated ResID.h file

1.12
----
Released 2014-12-25

- Added MD5 string (put at 0xA0) to the checksum command

1.11
----
Released 2014-11-20

- Supported filenames with space characters

1.10
----
Released 2014-09-25

- Added bmap command to generate binary formated map file.

1.00
----
Released 2013-08-22
- Added the support of :kind command in resouce list file.

0.99
----
Released 2013-03-28

- Added align option to map and link commands for specifying the number of
  alignment bytes.


0.12
----
Released 2013-03-22

- Added usb_head command to generate USB ISP header file of A1016
- Renamed usb_head command to checksum command
- Added padding option to link command
- Added filesize command to generate a filesize header file
- Appended newline on generated resource map files (e.g. ResMap.i)

0.02
----
Released 2013-2-27

- Initial version
- Added commands of link, map, and id

