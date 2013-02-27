@echo off
set reslnk=reslnk.exe

set src=res.lst
set tgt=res.bin
set dir=res
echo =^> Link resource files into single one.
%reslnk% link -d%dir% -o%tgt% %src%

set src=res.lst
set tgt=res_map.i
set dir=res
echo =^> Generate a resource map file in format of C array..
%reslnk% map -d%dir% -o%tgt% %src%

set src=res.lst
set tgt=ResID.h
echo =^> Generate a C header file of resource ID enumeration.
%reslnk% id -o%tgt% %src%

pause