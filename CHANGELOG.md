### 1.14 (2016-02-08)

- Extracted myutil.py from reslnk.py
- Added README.md
- Added CHANGELOG.md
- Added LICENSE.md
- Hosted to bitbucket.org
- Moved files for distribute.bat
- Removed filesize command
- Removed checksum command

### 1.13 (2015-04-07)

- Added allowing for *empty kinds* in generated ResID.h file

### 1.12 (2014-12-25)

- Added MD5 string (put at 0xA0) to the checksum command

### 1.11 (2014-11-20)
- Supported filenames with space characters

### 1.10 (2014-09-25)

- Added bmap command to generate binary formated map file.

### 1.00 (2013-08-22)

- Added the support of :kind command in resouce list file.

### 0.99 (2013-03-28)

- Added align option to map and link commands for specifying the number of
  alignment bytes.


### 0.12 (2013-03-22)

- Added usb_head command to generate USB ISP header file of A1016
- Renamed usb_head command to checksum command
- Added padding option to link command
- Added filesize command to generate a filesize header file
- Appended newline on generated resource map files (e.g. ResMap.i)

### 0.02 (2013-2-27)

- Initial version
- Added commands of link, map, and id

