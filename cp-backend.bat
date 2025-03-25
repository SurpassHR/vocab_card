@echo off

echo __pycache__> exclude.txt
xcopy /E /I /Y .\backend .\src-electron\dist-fastapi /EXCLUDE:exclude.txt
del exclude.txt