@echo off
set reslnk=reslnk.py

set src=res.map
set tgt=res.bin
set dir=res
echo =^> Link resource files into single one.
%reslnk% link -d%dir% -o%tgt% %src%

set src=res.map
set tgt=res_offset.i
set dir=res
echo =^> Generate a C included file listing offsets of resources.
%reslnk% offset -d%dir% -o%tgt% %src%

pause
