@echo off

REM check for required tools
where black >nul 2>nul || (echo Black is not installed. Aborting. & exit /b 1)
where isort >nul 2>nul || (echo Isort is not installed. Aborting. & exit /b 1)
where mypy >nul 2>nul || (echo Mypy is not installed. Aborting. & exit /b 1)
where flake8 >nul 2>nul || (echo Flake8 is not installed. Aborting. & exit /b 1)
where pylint >nul 2>nul || (echo Pylint is not installed. Aborting. & exit /b 1)

REM run black
echo Running Black...
black .
echo Black finished.
echo --------------------------------------

REM run isort
echo Running Isort...
isort .
echo Isort finished.
echo --------------------------------------

REM run mypy
echo Running Mypy...
mypy .
echo Mypy finished.
echo --------------------------------------

REM run flake8
echo Running Flake8...
flake8
echo Flake8 finished.
echo --------------------------------------

REM run pylint
echo Running Pylint...
pylint .
echo Pylint finished.
echo --------------------------------------

REM print message when each job is done
echo All linting and formatting jobs completed.
