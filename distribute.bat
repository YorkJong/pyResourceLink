@echo off

set target=reslnk
set ver_num=1.15
set dist_name=ResourceLink

set dist_dir=%dist_name%-%ver_num%-bin

if not exist %dist_dir% (
    md %dist_dir%
)
set _7z="C:\Program Files\7-Zip\7z.exe"

echo.
echo =^> Generating the executable file
cd bin
call clean.bat
cd ..
call build.bat %target% SkipPause

echo.
echo =^> Copying distributed files
xcopy /Y /E bin %dist_dir%\
del %dist_dir%\*test.bat
copy *.md %dist_dir%\*.txt

echo.
echo =^> Compressing distributed files
%_7z% a -tzip %dist_dir%.zip %dist_dir%\
rd /s /q %dist_dir%

pause
