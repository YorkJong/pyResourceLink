@echo off
set reslnk=reslnk.exe

set src=res.lst
set tgt=res.bin
set dir=res
echo =^> Link resource files into single one (%tgt%).
%reslnk% link -d%dir% -o%tgt% %src%

set src=res.lst
set tgt=ResMap.i
set dir=res
echo =^> Generate a resource map file (%tgt%) in format of C array.
%reslnk% map -d%dir% -o%tgt% %src%

set src=res.lst
set tgt=ResID.h
echo =^> Generate a C header file (%tgt%) of resource ID enumeration.
%reslnk% id -o%tgt% %src%

set src=fw.bin
set tgt=checksum.bin
echo =^> generate a checksum header file for the USB ISP of A1016
%reslnk% checksum -o%tgt% %src%


pause
