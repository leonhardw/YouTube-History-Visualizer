@echo off
set "UI_DIR=src/ui/resources"
set "PY_DIR=src/ui/generated"

for %%f in ("%UI_DIR%\*.ui") do (
    echo Converting: %%~nf.ui -^> ui_%%~nf.py
    pyside6-uic "%%f" -o "%PY_DIR%\ui_%%~nf.py"
)

echo.
echo All files saved to "%PY_DIR%".
pause