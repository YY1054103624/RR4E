# System Scripting Overview

## Python System Modules

**glob**

> For filename expansion

**socket**

> For network connections and Inter-Process Communication (IPC)

**threading, _thread, queue**

> For running and synchronizing concurrent threads

**time, timeit**

> For accessing system time details

**subprocess, multiprocessing**

> For launching and conrolling parallel process

**signal, select, shutil, temfile,** *and orhters*

> For various other system-related tasks

## Paging Documentation Strings

help(sys)

print(sys.\__doc__)

## A Custom Paging Script

*Example 2-1. PP4E\System\more.py*

```python
"""
split and interactively page a string or file of text
"""


def more(text, numlines=15):
    lines = text.splitlines()               # like split('\n') but no '' at end
    while lines:
        chunk = lines[:numlines]
        lines = lines[numlines:]
        for line in chunk: print(line)
        if lines and input('More?') not in ['y', 'Y']: break


if __name__ == '__main__':
    import sys                              # when run, not imported
    more(open(sys.argv[1]).read(), 10)      # page contents of file on cmdline

```

An alternative splitlines method does similar work, but retains an empty line at the end of the result if the last line is \n terminated:

```python
>>> line = 'aaa\nbbb\nccc\n'
>>> line.split('\n')
['aaa', 'bbb', 'ccc', '']
>>> line.splitlines()
['aaa', 'bbb', 'ccc']
```

## String Method Basics

```python
>>> mystr = 'xxxSPAMxxx'
>>> mystr.find('SPAM')
3
>>> mystr = 'xxaaxxaa'
>>> mystr.replace('aa', 'SPAM')
'xxSPAMxxSPAM'

>>> mystr = '\t Ni\n'
>>> mystr.strip() 				# remove whitespace
'Ni'
>>> mystr.rstrip() 			# same, but just on right side
'\t Ni'

>>> mystr.isalpha() 			# content tests
True
>>> mystr.isdigit()
False
>>> import string 			# case presets: for 'in', etc.
>>> string.ascii_lowercase
'abcdefghijklmnopqrstuvwxyz'
>>> string.whitespace 			# whitespace characters
' \t\n\r\x0b\x0c'

>>> delim = 'NI'
>>> delim.join(['aaa', 'bbb', 'ccc']) 	# join substrings list
'aaaNIbbbNIccc'
```

In fact, we can emulate the replace call we saw earlier in this section with a split/join combination:

```python
>>> mystr = 'xxaaxxaa'
>>> 'SPAM'.join(mystr.split('aa')) 		# str.replace, the hard way!
'xxSPAMxxSPAM'
```

## Other String Concepts in Python 3.X: Unicode and bytes

You generally know you are dealing with bytes if strings display or are coded with a leading “b” character before the opening quote (e.g., b'abc', '\xc4\xe8').

```python
open('file').read() 			# read entire file into string
open('file').read(N) 		# read next N bytes into string
open('file').readlines() 		# read entire file into line strings list
open('file').readline() 		# read next line, through '\n'
```

## Using Programs in Two Ways

This simple trick turns out to be one key to writing reusable script code: by coding program logic as functions rather than as top-level code, you can also import and reuse it in other scripts.

# Introduce the sys Modules Platforms and Versions

```python
>>> sys.platform, sys.maxsize, sys.version
('win32', 2147483647, '3.6.5 (v3.6.5:f59c0932b4, Mar 28 2018, 16:07:46) [MSC v.
1900 32 bit (Intel)]')
```

## The Module Search Path

**sys.path** is a list of directory name strings representing the true search path in a running Python interpreter. When a module is imported, Python scans this list from left to right, searching for the module’s file on each directory named in the list.

Python always uses the current sys.path setting to import, no matter what you’ve changed it to:

```python
>>> sys.path.append(r'C:\mydir')
>>> sys.path
['', 'C:\\PP4thEd\\Examples', ...more deleted..., 'C:\\mydir']
```

## The Loaded Modules Table

```python
>>> sys.modules
{'reprlib': <module 'reprlib' from 'c:\python31\lib\reprlib.py'>, ...more deleted...
```

## Exception Details

For instance, the **sys.exc_info** function returns a tuple with the latest exception’s type, value, and traceback object.

```python
>>> try:
... 	raise IndexError
... except:
... 	print(sys.exc_info())
...
(<class 'IndexError'>, IndexError(), <traceback object at 0x019B8288>)
```

The first two items returned by this call have reasonable string displays when printed directly, and the third is a traceback object that can be processed with the standard traceback module:

```python
>>> import traceback, sys
>>> def grail(x):
... 	raise TypeError('already got one')
...
>>> try:
... 	grail('arthur')
... except:
... 	exc_info = sys.exc_info()
... 	print(exc_info[0])
... 	print(exc_info[1])
... 	traceback.print_tb(exc_info[2])
...
<class 'TypeError'>
already got one
File "<stdin>", line 2, in <module>
File "<stdin>", line 2, in grail
```

# Introducing the os Module

## Administrative Tools

```python
>>> os.getpid()
7980
>>> os.getcwd()
'C:\\PP4thEd\\Examples\\PP4E\\System'
>>> os.chdir(r'C:\Users')
>>> os.getcwd()
'C:\\Users'
```

## Portability Constants

```python
>>> os.pathsep, os.sep, os.pardir, os.curdir, os.linesep
(';', '\\', '..', '.', '\r\n')
```

**os.pathsep** provides the character that sep-arates directories on directory lists, : for POSIX and ; for DOS and Windows.

## Common os.path Tools

The nested module **os.path** provides a large set of directory-related tools of its own.

```python
>>> os.path.isdir(r'C:\Users'), os.path.isfile(r'C:\Users')
(True, False)
>>> os.path.isdir(r'C:\config.sys'), os.path.isfile(r'C:\config.sys')
(False, True)
>>> os.path.isdir('nonesuch'), os.path.isfile('nonesuch')
(False, False)

>>> os.path.exists(r'c:\Users\Brian')
False
>>> os.path.exists(r'c:\Users\Default')
True
>>> os.path.getsize(r'C:\autoexec.bat')
24


>>> os.path.split(r'C:\temp\data.txt')
('C:\\temp', 'data.txt')

>>> os.path.join(r'C:\temp', 'output.txt')
'C:\\temp\\output.txt'

>>> name = r'C:\temp\data.txt' # Windows paths
>>> os.path.dirname(name), os.path.basename(name)
('C:\\temp', 'data.txt')

>>> name = '/home/lutz/temp/data.txt' # Unix-style paths
>>> os.path.dirname(name), os.path.basename(name)
('/home/lutz/temp', 'data.txt')

>>> os.path.splitext(r'C:\PP4thEd\Examples\PP4E\PyDemos.pyw')
('C:\\PP4thEd\\Examples\\PP4E\\PyDemos', '.pyw')


>>> os.sep
'\\'

>>> pathname = r'C:\PP4thEd\Examples\PP4E\PyDemos.pyw'
>>> os.path.split(pathname) # split file from dir
('C:\\PP4thEd\\Examples\\PP4E', 'PyDemos.pyw')

>>> pathname.split(os.sep) # split on every slash
['C:', 'PP4thEd', 'Examples', 'PP4E', 'PyDemos.pyw']

>>> os.sep.join(pathname.split(os.sep))
'C:\\PP4thEd\\Examples\\PP4E\\PyDemos.pyw'

>>> os.path.join(*pathname.split(os.sep))
'C:PP4thEd\\Examples\\PP4E\\PyDemos.pyw'
```

The **normpath** call comes in handy if your paths become a jumble of Unix and Windows separators:

```python
>>> mixed
'C:\\temp\\public/files/index.html'
>>> os.path.normpath(mixed)
'C:\\temp\\public\\files\\index.html'
>>> print(os.path.normpath(r'C:\temp\\sub\.\file.ext'))
C:\temp\sub\file.ext
```

## Running Shell commands from Scripts

The os module is also the place where we run shell commands from within Python scripts. Two os functions allow scripts to run any command line that you can type in a console window

**os.system**

> Runs a shell command from a Python script

**os.popen**

> Runs a shell command and connects to its input or output streams

### What's a shell commands?

Here are two shell commands typed and run in an MS-DOS console box on Windows:

```powershell
C:\...\PP4E\System> dir /B 		...type a shell command line
helloshell.py 					...its output shows up here
more.py 						...DOS is the shell on Windows
more.pyc
spam.txt
__init__.py

C:\...\PP4E\System> type helloshell.py
# a Python program
print('The Meaning of Life')
```
### Running shell commands
```python
>>> import os
>>> os.system('dir /B')
helloshell.py
more.py
more.pyc
spam.txt
__init__.py
0
>>> os.system('type helloshell.py')
# a Python program
print('The Meaning of Life')
0

>>> os.system('type hellshell.py')
The system cannot find the file specified.
1
```
### Communicating with shell commands
```python
>>> open('helloshell.py').read()
"# a Python program\nprint('The Meaning of Life')\n"

>>> text = os.popen('type helloshell.py').read()
>>> text
"# a Python program\nprint('The Meaning of Life')\n"

>>> listing = os.popen('dir /B').readlines()
>>> listing
['helloshell.py\n', 'more.py\n', 'more.pyc\n', 'spam.txt\n', '__init__.py\n']
```
So far, weve run basic DOS commands; because these calls can run any command line that we can type at a shell prompt, they can also be used to launch other Python scripts.
```python
>>> os.system('python helloshell.py') # run a Python program
The Meaning of Life
0
>>> output = os.popen('python helloshell.py').read()
>>> output
'The Meaning of Life\n'
```
### The subprocess module alternative
As mentioned, in recent releases of Python the subprocess module can achieve the same effect as os.system and os.popen;
```python
>>> import subprocess
>>> subprocess.call('python helloshell.py') # roughly like os.system()
The Meaning of Life
0
>>> subprocess.call('cmd /C "type helloshell.py"') # built-in shell cmd
# a Python program
print('The Meaning of Life')
0
>>> subprocess.call('type helloshell.py', shell=True) # alternative for built-ins
# a Python program
print('The Meaning of Life')
0
```
Notice the **shell=True** in the last command here. This is a subtle and platform-dependent requirement:
- On Windows, we need to pass a **shell=True** argument to **subprocess** tools like call and Popen (shown ahead) in order to run commands built into the shell. Win- dows commands like type require this extra protocol, but normal executables like python do not.
- On Unix-like platforms, when **shell** is **False** (its default), the program command line is run directly by **os.execvp**, a call well meet in Chapter 5. If this argument is True, the command-line string is run through a shell instead, and you can specify the shell to use with additional arguments.

Besides imitating **os.system**, we can similarly use this module to emulate the **os.popen** call used earlier, to run a shell command and obtain its standard output text in our script:
```python
>>> pipe = subprocess.Popen('python helloshell.py', stdout=subprocess.PIPE)
>>> pipe.communicate()
(b'The Meaning of Life\r\n', None)
>>> pipe.returncode
0
```
```python
>>> pipe = subprocess.Popen('python helloshell.py', stdout=subprocess.PIPE)
>>> pipe.stdout.read()
b'The Meaning of Life\r\n'
>>> pipe.wait()
0
```
In fact, there are direct mappings from **os.popen** calls to subprocess.Popen objects:
```python
>>> from subprocess import Popen, PIPE
>>> Popen('python helloshell.py', stdout=PIPE).communicate()[0]
b'The Meaning of Life\r\n'
>>>
>>> import os
>>> os.popen('python helloshell.py').read()
'The Meaning of Life\n'
```
### Shell command limitations
Second, it is important to remember that running Python files as programs this way is very different and generally much slower than importing program files and calling functions they define.
In fact, this is so useful that an os.startfile call was added in recent Python releases.
```python
os.startfile("webpage.html")    # open file in your web browser
os.startfile("document.doc")    # open file in Microsoft Word
os.startfile("myscript.py")     # run file with Python
```
## Other os Module Exports
**os.environ**
> Fetches and sets shell environment variables

**os.fork**
> Spawns a new child process on Unix-like systems

**os.pipe**
> Communicates between programs

**os.execlp**
> Starts new programs

**os.spawnv**
> Starts new programs with lower-level control

**os.open**
> Opens a low-level descriptor-based file

**os.mkdir**
> Creates a new directory

**os.mkfifo**
> Creates a new named pipe

**os.stat**
> Fetchs low-level file information

**os.remove**
> Deletes a file by its pathname

**os.walk**
> Applies a function or loop body to all parts of an entire directory tree
#### subprocess, os.popen, and Iterators
The **os.popen** result is an object that manages the **Popen** object and its piped stream:
```python
>>> I = os.popen('dir /B *.py')
>>> I.__next__()
'helloshell.py\n'

>>> I = os.popen('dir /B *.py')
>>> next(I)
TypeError: _wrap_close object is not an iterator
```
The reason for this is subtledirect __next__ calls are intercepted by a __getattr__ defined in the pipe wrapper object, and are properly delegated to the wrapped object; but next function calls invoke Pythons operator overloading machinery, which in 3.X bypasses the wrappers __getattr__ for special method names like __next__. Since the pipe wrapper object doesnt define a __next__ of its own, the call is not caught and delegated.
```python
>>> I = os.popen('dir /B *.py')
>>> I = iter(I) # what for loops do
>>> I.__next__() # now both forms work
'helloshell.py\n'
>>> next(I)
'more.py\n'
```
