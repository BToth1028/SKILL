@echo off
setlocal

cd /d "%~dp0"
python "%~dp0load_typedb_snapshot_search.py" %*
if errorlevel 1 exit /b %ERRORLEVEL%

rem cd into this script dir, run the sibling loader, propagate errorlevel.
rem This pipeline only updates the Qdrant directive-mcp-search collection.

exit /b 0
