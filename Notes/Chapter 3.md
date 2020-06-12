# "I'd Like to Have an Argument, Please"
*Current working directory*
> **os.getcwd** gives access to the directory from which a script is started, and many file tools use its value implicitly.

*Command-line arguments*
> **sys.argv** gives access to words typed on the command line that are used to start the program and that serve as script inputs.

*Shell variables*
> **os.environ** provides an interface to names assigned in the enclosing shell (or a parent program) and passed in to the script.

*Standard streams*
> **sys.stdin**, **stdout**, and **stderr** .

# Current Working Directory
## CWD, Files, and Import Paths
When you run a Python script by typing a shell command line such as python dir1\dir2\file.py, the CWD is the directory you were in when you typed this command, not dir1\dir2. On the other hand, Python automatically adds the identity of the script's home directory to the front of the module search path such that file.py can always import other files in dir1\dir2 no matter where it is run from.
```python
C:\...\PP4E\System> type whereami.py
import os, sys
print('my os.getcwd =>', os.getcwd()) # show my cwd execution dir
print('my sys.path =>', sys.path[:6]) # show first 6 import paths
input()
```
```python
C:\...\PP4E\System> set PYTHONPATH=C:\PP4thEd\Examples
C:\...\PP4E\System> python whereami.py
my os.getcwd => C:\...\PP4E\System
my sys.path => ['C:\\...\\PP4E\\System', 'C:\\PP4thEd\\Examples', ...more... ]
```
```python
C:\...\PP4E\System> cd ..
C:\...\PP4E> python System\whereami.py
my os.getcwd => C:\...\PP4E
my sys.path => ['C:\\...\\PP4E\\System', 'C:\\PP4thEd\\Examples', ...more... ]
```

