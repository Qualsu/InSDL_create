@echo off

set /p folder_name="Project name: "

set /p add_vsc="add .vscode folder? (y/n): "

set /p add_bat="add compile.bar file? (y/n): "

if /i "%add_vsc%"=="y" (
    set vsc_flag=-vsc
) else (
    set vsc_flag=
)

if /i "%add_bat%"=="y" (
    set bat_flag=-bat
) else (
    set bat_flag=
)

python main.py create "%folder_name%" %vsc_flag% %bat_flag%

pause