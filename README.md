# LangConvert #

LangConvert is an open source Python application to link resource files into
single one (*link* command). It also provides *map* command to generate a
resource map file in C array style, *bmap* command to generate the resource map
file in binary style, and *id* command to generate a C header file of resource
ID enumeration.


## Install ##

1. Download a binary distribution of ResourceLink (e.g.,
   *ResourceLink-1.14-bin.zip*) from [Downloads][] page.
2. Uncompress the binary distribution.

[Downloads]: https://bitbucket.org/YorkJong/pyresourcelink/downloads


## Getting Started ##

1. Install ResourceLink.
2. Put resource files to the *res* folder.
3. Edit the *res.lst* file.
4. Run `demo.bat` to generate *res.bin*, *ResMap.i*, *ResMap.bin*, and
   *ResID.h*.
    - *res.bin* is generated with **link** command.
    - *ResMap.i* is generated with **map** command.
    - *ResMap.bin* is generated with **bmap** command.
    - *ResID.h* is generated with **id** command.
5. Run `clean.bat` to remove generated files.

### The sample *res.lst* ###
```sh
:0x00       # start offset (default is 0x00)

:kind=B     # kind B for the enumeration
bat.png     # file size: 2877 bytes

:4096       # offset to address: 4096
broom.png   # file size: 3083 bytes

:kind=C1
:kind=C2

:kind=D
candle.png  # file size: 2771 bytes

:kind=E1
:kind=E2
```
- This file is used to list filenames of resources.
- A `#` denotes a comment begins after the `#` and ends at the end of the line.
- A line prefixing `:<number>` denotes an byte alignment of next resource when
  linking.
    - The <number> can be a decimal number or a hexadecimal number (begins
      with `0x`)
    - The `:4096` prefixing `broom.png` means *broom.png* will put on offset
      4096 bytes of the linking file.
- A line prefixing `:kind` works only on *id* command and is used to classify
  generated enumerators.
    - see the documentation of *generated ResID.h* for details

### generated *ResMap.i* ###
```c
// Generated by the Resource Link v1.14
//    !author: Jiang Yu-Kuan <yukuan.jiang@gmail.com>
//    !trail: reslnk.exe map -dres -oResMap.i -a4 res.lst

//   offset,       size     (in bytes)
{         0,       2877},   // RES_PNG_bat (bat.png)
{      4096,       3083},   // RES_PNG_broom (broom.png)
{      7180,       2771},   // RES_PNG_candle (candle.png)
```
* You can apply a generated *ResMap.i* with a C `struct` to read the content of
  a resource.

### An example C struc with *ResMap.i* looks like as follows: ###
```c
#include "ResID.h"


/** Resource Map (a list of offset-size pairs) */
static struct {
    uint32_t offset;    ///< offset of a resource
    uint32_t nBytes;    ///< total bytes of a resource
} _resMap[] = {
    #include "ResMap.i"
};


/** Returns address in NOR Flash that stores the resource. */
Addr Res_Addr(ResID id)
{
    assert (id < RES_End);

    Res_initMapTblIfHasNotDone();
    return _resMap[id].offset + _baseAddr;
}


/** Returns total bytes of a resource. */
uint32_t Res_Bytes(ResID id)
{
    assert (id < RES_End);

    Res_initMapTblIfHasNotDone();
    return _resMap[id].nBytes;
}
```


### generated *ResID.h* ###
```c
// Generated by the Resource Link v1.14
//    !author: Jiang Yu-Kuan <yukuan.jiang@gmail.com>
//    !trail: reslnk.exe id -oResID.h res.lst
#ifndef _RES_ID_H
#define _RES_ID_H


/** IDs of Resources */
typedef enum {
    RES_B_BEGIN,
    RES_PNG_bat = RES_B_BEGIN,
    RES_PNG_broom,
    RES_B_END,

    RES_C1_BEGIN = RES_B_END,
    RES_C1_END = RES_C1_BEGIN,

    RES_C2_BEGIN = RES_C1_END,
    RES_C2_END = RES_C2_BEGIN,

    RES_D_BEGIN = RES_C2_END,
    RES_PNG_candle = RES_D_BEGIN,
    RES_D_END,

    RES_E1_BEGIN = RES_D_END,
    RES_E1_END = RES_E1_BEGIN,

    RES_E2_BEGIN = RES_E1_END,
    RES_E2_END = RES_E2_BEGIN,

    RES_End = RES_E2_END,
    RES_Total = RES_End
} ResID;


#endif // _RES_ID_H
```
- The `RES_B_BEGIN` and `RES_B_END` are relative to the `:kind=B` in *res.lst*
  file.


## Command Line ##
### Top level ###
```
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
```

### link command ###
```
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
```

### map command ###
```
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
```

### bmap command ###
```
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
```

### id command ###
```
usage: reslnk.exe id [-h] [-o <file>] lst-file

positional arguments:
  lst-file              The list file of resources.

optional arguments:
  -h, --help            show this help message and exit
  -o <file>, --output <file>
                        place the output into <file>, the C header file of
                        resource ID enumeration (default "ResID.h").
```

