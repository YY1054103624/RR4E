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
The net effects is that filenames without directory paths in a script will be mapped to the place where the *command* was typed(**os.getcwd**), but imports still have access to the directory of the *script* being run (via the front of sys.path). The following output, for example, appears in a new DOS console box when whereami.py is double-clicked in Windows Explorer:
# Command-Line Arguments
```python
>>> import sys
>>> sys.argv
```
*Example 3-1. PP4E\System\testargv.py*
```python
import sys
print(sys.argv)
```
```python
C:\...\PP4E\System> python testargv.py
['testargv.py']

C:\...\PP4E\System> python testargv.py spam eggs cheese
['testargv.py', 'spam', 'eggs', 'cheese']

C:\...\PP4E\System> python testargv.py -i data.txt -o results.txt
['testargv.py', '-i', 'data.txt', '-o', 'results.txt']
```
The last command here illustrates a common convention. Much like function argu- ments, command-line options are sometimes passed by position and sometimes by name using a “-name value” word pair.
# Shell Environment Variables
## Fetching Shell Variables
```python
>>> import os
>>> os.environ.keys()
KeysView(<os._Environ object at 0x013B8C70>)

>>> list(os.environ.keys())
['TMP', 'COMPUTERNAME', 'USERDOMAIN', 'PSMODULEPATH', 'COMMONPROGRAMFILES',
...many more deleted...
'NUMBER_OF_PROCESSORS', 'PROCESSOR_LEVEL', 'USERPROFILE', 'OS', 'PUBLIC', 'QTJAVA']

>>> os.environ['TEMP']
'C:\\Users\\mark\\AppData\\Local\\Temp'
```
```shell script
set PYTHONPATH=C:\PP4thEd\Examples;C:\Users\Mark\temp
```
```python
>>> os.environ['PYTHONPATH']
'C:\\PP4thEd\\Examples;C:\\Users\\Mark\\temp'

>>> for srcdir in os.environ['PYTHONPATH'].split(os.pathsep):
... print(srcdir)
...
C:\PP4thEd\Examples
C:\Users\Mark\temp

>>> import sys
>>> sys.path[:3]
['', 'C:\\PP4thEd\\Examples', 'C:\\Users\\Mark\\temp']
```
**PYTHONPATH** is a string of directory paths separated by whatever character is used to separate items in such paths on your platform (e.g., **;** on DOS/Windows, **:** on Unix and Linux).
## Changing Shell Variables
Like normal dictionaries, the **os.environ** object supports both key indexing and *assignment*.
```python
>>> os.environ['TEMP']
'C:\\Users\\mark\\AppData\\Local\\Temp
>>> os.environ['TEMP'] = r'c:\temp'
>>> os.environ['TEMP']
'c:\\temp'
```
*Example 3-3. PP4E\System\Environment\setenv.py*
```python
import os
print('setenv...', end=' ')
print(os.environ['USER'])               # show current shell variable value


os.environ['USER'] = 'Brian'            # runs os.putenv behind the scenes
os.system('python echoenv.py')

os.environ['USER'] = 'Arthur'           # changes passed to spawned programs
os.system('python echoenv.py')          # and linked-in C library modules

os.environ['USER'] = input('?')
print(os.popen('python echoenv.py').read())
```
This setenv.py script simply changes a shell variable, **USER**, and spawns another script that echoes this variable’s value, as shown in Example 3-4.

*Example 3-4. PP4E\System\Environment\echoenv.py*
```python
import os
print('echoenv...', end=' ')
print('Hello,', os.environ['USER'])
```
No matter how we run echoenv.py, it displays the value of **USER** in the enclosing shell;
```python
C:\...\PP4E\System\Environment> set USER=Bob

C:\...\PP4E\System\Environment> python echoenv.py
echoenv... Hello, Bob
```
```python
C:\...\PP4E\System\Environment> python setenv.py
setenv... Bob
echoenv... Hello, Brian
echoenv... Hello, Arthur
?Gumby
echoenv... Hello, Gumby

C:\...\PP4E\System\Environment> echo %USER%
Bob
```
## Shell Variable Fine Points: Parents, putenv, and getenv
# Standard Streams
The **sys** module is also the place where the standard input, output, and error streams of your Python programs live;
```python
>>> for f in (sys.stdin, sys.stdout, sys.stderr):
...     print(f)
...
<_io.TextIOWrapper name='<stdin>' mode='r' encoding='utf-8'>
<_io.TextIOWrapper name='<stdout>' mode='w' encoding='utf-8'>
<_io.TextIOWrapper name='<stderr>' mode='w' encoding='utf-8'>
```
Because the **print** and **input** built-in functions are really nothing more than user- friendly interfaces to the standard output and input streams, they are similar to using **stdout** and **stdin** in **sys** directly:
```python
>>> print('hello stdout world')
hello stdout world

>>> sys.stdout.write('hello stdout world' + '\n')
hello stdout world
19

>>> input('hello stdin world>')
hello stdin world>spam
'spam'

>>> print('hello stdin world>'); sys.stdin.readline()[:-1]
hello stdin world>
eggs
'eggs'
```
### Standard Streams on Windows
The *.pyw* extension simply means a *.py* source file without a DOS pop up on Windows (it uses Windows registry settings to run a custom version of Python). A *.pyw* file may also be imported as usual.
## Redirecting Streams to Files and Programs
*Example 3-5. PP4E\System\Streams\teststreams.py*
```python
"read numbers till eof and show squares"


def interact():
    print('Hello stream world')
    while True:
        try:
            reply = input('Enter a number>')
        except EOFError:
            break
        else:
            num = int(reply)
            print('%d squared is %d' % (num, num ** 2))
    print('Bye')


if __name__ == '__main__':
    interact()
```
```shell script
C:\...\PP4E\System\Streams> python teststreams.py
Hello stream world
Enter a number>12
12 squared is 144
Enter a number>10
10 squared is 100
Enter a number>^Z
Bye
```
But on both Windows and Unix-like platforms, we can redirect the standard input stream to come from a file with the **< filename** shell syntax.
```shell script
C:\...\PP4E\System\Streams> type input.txt
8
6

C:\...\PP4E\System\Streams> python teststreams.py < input.txt
Hello stream world
Enter a number>8 squared is 64
Enter a number>6 squared is 36
Enter a number>Bye
```
### Chaining programs with pipes
Let’s send the output of the Python script to the standard **more** command-line program’s input to see how this works:
```shell script
C:\...\PP4E\System\Streams> python teststreams.py < input.txt | more
Hello stream world
Enter a number>8 squared is 64
Enter a number>6 squared is 36
Enter a number>Bye
```
Because Python ties scripts into the standard stream model, though, Python scripts can be used on both ends. One Python script’s output can always be piped into another Python script’s input:
```shell script
C:\...\PP4E\System\Streams> type writer.py
print("Help! Help! I'm being repressed!")
print(42)

C:\...\PP4E\System\Streams> type reader.py
print('Got this: "%s"' % input())
import sys
data = sys.stdin.readline()[:-1]
print('The meaning of life is', data, int(data) * 2)

C:\...\PP4E\System\Streams> python writer.py
Help! Help! I'm being repressed!
42

C:\...\PP4E\System\Streams> python writer.py | python reader.py
Got this: "Help! Help! I'm being repressed!"
The meaning of life is 42 84
```
*Example 3-6. PP4E\System\Streams\sorter.py*
```python
import sys                                  # or sorted(sys.stdin)
lines = sys.stdin.readlines()               # sort stdin input lines,
lines.sort()                                # send result to stdout
for line in lines: print(line, end='')      # for further processing
```
*Example 3-7. PP4E\System\Streams\adder.py*
```python
import sys
sum = 0
while True:
    try:
        line = input()                  # or call sys.stdin.readlines()
    except EOFError:                    # or for line in sys.stdin:
        break                           # input strips \n at end
    else:
        sum += int(line)                # was string.atoi() in 2nd ed
print(sum)        
```
```shell script
C:\...\PP4E\System\Streams> type data.txt
123
000
999
042

C:\...\PP4E\System\Streams> python sorter.py < data.txt sort a file
000
042
123
999

C:\...\PP4E\System\Streams> python adder.py < data.txt sum file
1164

C:\...\PP4E\System\Streams> type data.txt | python adder.py sum type output
1164

C:\...\PP4E\System\Streams> type writer2.py
for data in (123, 0, 999, 42):
print('%03d' % data)

C:\...\PP4E\System\Streams> python writer2.py | python sorter.py sort py output
000
042
123
999

C:\...\PP4E\System\Streams> writer2.py | sorter.py shorter form
...same output as prior command on Windows...

C:\...\PP4E\System\Streams> python writer2.py | python sorter.py | python adder.py
1164
```
### Coding alternative for adders and sorters
```shell script
C:\...\PP4E\System\Streams> type adder2.py
import sys
sum = 0
while True:
    line = sys.stdin.readline()
    if not line: break
    sum += int(line)
print(sum)
```
This version utilizes the fact that **int** allows the digits to be surrounded by whitespace (**readline** returns a line including its **\n**, but we don’t have to use **[:-1]** or **rstrip()** to remove it for **int**).
```shell script
C:\...\PP4E\System\Streams> type adder3.py
import sys
sum = 0
for line in sys.stdin: sum += int(line)
print(sum)
```
The following work the same way as the originals, with noticeably less source-file real estate:
```shell script
C:\...\PP4E\System\Streams> type sorterSmall.py
import sys
for line in sorted(sys.stdin): print(line, end='')

C:\...\PP4E\System\Streams> type adderSmall.py
import sys
print(sum(int(line) for line in sys.stdin))
```
## Redirected Streams and User Interaction
For example, if we change the last three lines of the *more.py* file listed as Example 2-1 in the prior chapter…
```python
if __name__ == '__main__': # when run, not when imported
    import sys
    if len(sys.argv) == 1: # page stdin if no cmd args
        more(sys.stdin.read())
    else:
        more(open(sys.argv[1]).read())
```
```shell script
C:\...\PP4E\System\Streams> python teststreams.py < input.txt | python ..\more.py
Hello stream world
Enter a number>8 squared is 64
Enter a number>6 squared is 36
Enter a number>Bye
```
But there’s a subtle problem lurking in the preceding **more.py** command. Really, chain- ing worked there only by sheer luck: if the first script’s output is long enough that **more** has to ask the user if it should continue, the script will utterly fail (specifically, when **input** for user interaction triggers **EOFError**).

*Example 3-8. PP4E\System\Streams\moreplus.py*
```python
"""
split and interactively page a string, file, or stream of
text to stdout; when run as a script, page stdin or file
whose name is passed on cmdline; if input is stdin, can't
use it for user reply--use platform-specific tools or GUI;
"""


import sys


def getreply():
    """
    read a reply key from an interactive user
    even if stdin redirected to a file or pipe
    """
    if sys.stdin.isatty():                      # if stdin is console
        return input('?')                       # read reply line from stdin
    else:
        if sys.platform[:3] == 'win':           # if stdin is redirected
            import msvcrt                       # can't use to ask a user
            msvcrt.putch(b'?')
            key = msvcrt.getche()               # use windows console tools
            msvcrt.putch(b'\n')                 # getch() does not echo key
            return key
        else:
            assert False, 'platform not supported'
            #linux?:  open('/dev/tty').readline()[:-1]


def more(text, numlines=15):
    """
    page multiline string to stdout
    """
    lines = text.splitlines()
    while lines:
        chunk = lines[:numlines]
        lines = lines[numlines:]
        for line in chunk: print(line)
        if lines and input('More?') not in ['y', 'Y']: break


if __name__ == '__main__':                      # when run, not when imported
    if len(sys.argv) == 1:                      # if no command-line arguments
        more(sys.stdin.read())                  # page stdin, no inputs
    else:
        more(open(sys.argv[1]).read())          # else page filename argument
```
The file’s **isatty** method tells us whether **stdin** is connected to the console; if it is, we simply read replies on **stdin** as before.

As before, we can import and call this module’s function directly, passing in whatever string we wish to page:
```python
>>> from moreplus import more
>>> more(open('adderSmall.py').read())
import sys
print(sum(int(line) for line in sys.stdin))
```

Also as before, when run with a command-line *argument*, this script interactively pages through the named file’s text:
```shell script
C:\...\PP4E\System\Streams> python moreplus.py adderSmall.py
import sys
print(sum(int(line) for line in sys.stdin))

C:\...\PP4E\System\Streams> python moreplus.py moreplus.py
"""
split and interactively page a string, file, or stream of
text to stdout; when run as a script, page stdin or file
whose name is passed on cmdline; if input is stdin, can't
use it for user reply--use platform-specific tools or GUI;
"""


import sys

def getreply():
?n
```
## Redirecting Streams to Python Objects
That is:
* Any object that provides file-like *read* methods can be assigned to **sys.stdin** to make input come from that object’s read methods.
* Any object that defines file-like *write* methods can be assigned to **sys.stdout**; all standard output will be sent to that object’s methods.

**print** and **input** simply call the **write** and **readline** methods

*Example 3-9. PP4E\System\Streams\redirect.py*
```python
"""
file-like objects that save standard output text in a string and provide
standard input text from a string; redirect runs a passed-in function
with its output and input streams reset to these file-like class objects;
"""


import sys                                  # get built-in modules


class Output:                               # simulated output file
    def __init__(self):
        self.text = ''                      # empty string when created

    def write(self, string):                # add a string of bytes
        self.text += string

    def writelines(self, lines):            # add each line in a list
        for line in lines: self.write(line)


class Input:                                # simulated input file
    def __init__(self, input=''):           # default argument
        self.text = input

    def read(self, size=None):              # save string when created
        if size == None:                    # read N bytes, or all
            res, self.text = self.text, ''
        else:
            res, self.text = self.text[:size], self.text[size:]
        return res

    def readline(self):
        eoln = self.text.find('\n')         # find offset of next eoln
        if eoln == -1:                      # slice off through eoln
            res, self.text = self.text, ''
        else:
            res, self.text = self.text[:eoln+1], self.text[eoln+1:]
        return res


def redirect(function, pargs, kargs, input):    # redirect stdin/out
    savestreams = sys.stdin, sys.stdout         # run a function object
    sys.stdin = Input(input)                    # return stdout text
    sys.stdout = Output()
    try:
        result = function(*pargs, **kargs)      # run function with args
        output = sys.stdout.text
    finally:
        sys.stdin, sys.stdout = savestreams     # restore if exc or not
    return (result, output)                     # return result if no exc
```

When run directly, the function reads from the keyboard and writes to the screen, just as if it were run as a program without redirection:

```shell script
C:\...\PP4E\System\Streams> python
>>> from teststreams import interact
>>> interact()
Hello stream world
Enter a number>2
2 squared is 4
Enter a number>3
3 squared is 9
Enter a number^Z
Bye
>>>
```

```python
>>> from redirect import redirect
>>> (result, output) = redirect(interact, (), {}, '4\n5\n6\n')
>>> print(result)
None
>>> output
'Hello stream world\nEnter a number>4 squared is 16\nEnter a number>5 squared
is 25\nEnter a number>6 squared is 36\nEnter a number>Bye\n'
```

```python
>>> for line in output.splitlines(): print(line)
...
Hello stream world
Enter a number>4 squared is 16
Enter a number>5 squared is 25
Enter a number>6 squared is 36
Enter a number>Bye
```

## The io.StringIO and io.BytesIO Utility Classes

```python
>>> from io import StringIO
>>> buff = StringIO() # save written text to a string
>>> buff.write('spam\n')
5
>>> buff.write('eggs\n')
5
>>> buff.getvalue()
'spam\neggs\n'

>>> buff = StringIO('ham\nspam\n') # provide input from a string
>>> buff.readline()
'ham\n'
>>> buff.readline()
'spam\n'
>>> buff.readline()
''
```

As in the prior section, instances of **StringIO** objects can be assigned to **sys.stdin** and **sys.stdout** to redirect streams for **input** and **print** calls and can be passed to any code that was written to expect a real file object.

```python
>>> from io import StringIO
>>> import sys
>>> buff = StringIO()

>>> temp = sys.stdout
>>> sys.stdout = buff
>>> print(42, 'spam', 3.141) # or print(..., file=buff)
>>> sys.stdout = temp # restore original stream
>>> buff.getvalue()
'42 spam 3.141\n'
```

Note that there is also an **io.BytesIO** class with similar behavior, but which maps file operations to an in-memory bytes buffer, instead of a **str** string:

## Capturing the stderr Stream

Redirecting standard errors from a shell command line is a bit more complex and less portable. On most Unix-like systems, we can usually capture **stderr** output by using shell-redirection syntax of the form **command > output 2>&1**.

## Redirection Syntax in Print Calls

```python
print(stuff, file=afile) # afile is an object, not a string name
```

```python
import sys
print('spam' * 2, file=sys.stderr)
```

Similarly, we can use either our custom class or the standard library’s class as the output file with this hook:

```python
>>> from io import StringIO
>>> buff = StringIO()
>>> print(42, file=buff)
>>> print('spam', file=buff)
>>> print(buff.getvalue())
42
spam
>>> from redirect import Output
>>> buff = Output()
>>> print(43, file=buff)
>>> print('eggs', file=buff)
>>> print(buff.text)
43
eggs
```

## Other Redirection Options: os.popen and subprocess Revisited

### Redirecting input or output with os.popen

```python
C:\...\PP4E\System\Streams> type hello-out.py
print('Hello shell world')

C:\...\PP4E\System\Streams> type hello-in.py
inp = input()
open('hello-in.txt', 'w').write('Hello ' + inp + '\n')
```

These scripts can be run from a system shell window as usual:

```python
C:\...\PP4E\System\Streams> python hello-out.py
Hello shell world

C:\...\PP4E\System\Streams> python hello-in.py
Brian

C:\...\PP4E\System\Streams> type hello-in.txt
Hello Brian
```

As we saw in the prior chapter, Python scripts can read *output* from other programs and scripts like these, too, using code like the following:

```python
C:\...\PP4E\System\Streams> python
>>> import os
>>> pipe = os.popen('python hello-out.py') # 'r' is default--read stdout
>>> pipe.read()
'Hello shell world\n'
>>> print(pipe.close()) # exit status: None is good
None
```

But Python scripts can also provide *input* to spawned programs’ standard input streams—passing a “w” mode argument, instead of the default “r”, connects the re- turned object to the spawned program’s input stream.

```python
>>> pipe = os.popen('python hello-in.py', 'w') # 'w'--write to program stdin
>>> pipe.write('Gumby\n')
6
>>> pipe.close() # \n at end is optional
>>> open('hello-in.txt').read() # output sent to a file
'Hello Gumby\n'
```

### Redirecting input and output with subprocess

```python
C:\...\PP4E\System\Streams> python
>>> from subprocess import Popen, PIPE, call
>>> X = call('python hello-out.py') # convenience
Hello shell world
>>> X
0

>>> pipe = Popen('python hello-out.py', stdout=PIPE)
>>> pipe.communicate()[0] # (stdout, stderr)
b'Hello shell world\r\n'
>>> pipe.returncode # exit status
0

>>> pipe = Popen('python hello-out.py', stdout=PIPE)
>>> pipe.stdout.read()
b'Hello shell world\r\n'
>>> pipe.wait() # exit status
0
```

```python
>>> pipe = Popen('python hello-in.py', stdin=PIPE)
>>> pipe.stdin.write(b'Pokey\n')
6
>>> pipe.stdin.close()
>>> pipe.wait()
0
>>> open('hello-in.txt').read() # output sent to a file
'Hello Pokey\n'
```

In fact, we can use obtain *both the input and output* streams of a spawned program with this module. Let’s reuse the simple writer and reader scripts we wrote earlier to demonstrate:

```shell script
C:\...\PP4E\System\Streams> type writer.py
print("Help! Help! I'm being repressed!")
print(42)

C:\...\PP4E\System\Streams> type reader.py
print('Got this: "%s"' % input())
import sys
data = sys.stdin.readline()[:-1]
print('The meaning of life is', data, int(data) * 2)
```

```python
>>> pipe = Popen('python reader.py', stdin=PIPE, stdout=PIPE)
>>> pipe.stdin.write(b'Lumberjack\n')
11
>>> pipe.stdin.write(b'12\n')
3
>>> pipe.stdin.close()
>>> output = pipe.stdout.read()
>>> pipe.wait()
0
>>> output
b'Got this: "Lumberjack"\r\nThe meaning of life is 12 24\r\n'
```

```python
C:\...\PP4E\System\Streams> python writer.py | python reader.py
Got this: "Help! Help! I'm being repressed!"
The meaning of life is 42 84

C:\...\PP4E\System\Streams> python
>>> from subprocess import Popen, PIPE
>>> p1 = Popen('python writer.py', stdout=PIPE)
>>> p2 = Popen('python reader.py', stdin=p1.stdout, stdout=PIPE)
>>> output = p2.communicate()[0]
>>> output
b'Got this: "Help! Help! I\'m being repressed!"\r\nThe meaning of life is 42 84\r\n'
>>> p2.returncode
0
```

We can get close to this with **os.popen**, but that the fact that its pipes are read or write (and not both) prevents us from catching the second script’s output in our code:

```python

```
