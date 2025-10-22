# Pachlib
A Python library full of useful tools, such as SSH, loading bars, and dynamic library importing (with pip).

# How to add it to your project?
**NOTE: When pachlib is mentioned in this section, it's referring to the pachlib folder INSIDE the Pachlib_vX.X folder.**
**There are more ways to install pachlib than these ones, but in the future it might be directly installed with pip.**

## 1. Same folder import
Put pachlib on the same folder as your python program and then do:
`import pachlib`

## 2. Add to PYTHONPATH with sys
Add pachlib to the Python Path by doing:
`import sys`
`sys.path.append(/path/to/pachlib)`
Replacing /path/to/pachlib with the path to pachlib (Make sure you don't move it or change its name)

## 3. Add to PYTHONPATH manually
Open your terminal and run:
`set PYTHONPATH=C:/path/to/pachlib;%PYTHONPATH%` (Windows)
`export PYTHONPATH=/path/to/pachlib:$PYTHONPATH` (Linux / macOS)
Replacing /path/to/pachlib with the path to pachlib (Make sure you don't move it or change its name)

## 4. Add to site-packages
To see where the site-packages folder is, make a python file with this code:
`import site`
`print(site.getsitepackages())`
The run it, it should return a list with the path to the site-packages folder.
Now, move pachlib to that folder.
