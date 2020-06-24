# File Tools

## The File Object Model in Python 3.X

## Using Built-in File Objects

### Output files

File **write** calls return the number of characters or bytes written (which we’ll sometimes omit in this book to save space), and as we’ll see, **close** calls are often optional, unless you need to open and read the file again during the same program or session:

```python
C:\temp> python
>>> file = open('data.txt', 'w') # open output file object: creates
>>> file.write('Hello file world!\n') # writes strings verbatim
18
>>> file.write('Bye file world.\n') # returns number chars/bytes written
18
>>> file.close()
```

And that’s it—you’ve just generated a brand-new text file on your computer, regardless of the computer on which you type this code:

```shell script
C:\temp> dir data.txt /B
data.txt

C:\temp> type data.txt
Hello file world!
Bye file world.
```

**Writing.** Notice that we added an explicit **\n** end-of-line character to lines written to the file; unlike the **print** built-in function, file object **write** methods write exactly what they are passed without adding any extra formatting. 

Output files also sport a **writelines** method, which simply writes all of the strings in a list one at a time without adding any extra formatting. For example, here is a **write lines** equivalent to the two **write** calls shown earlier:

```python
file.writelines(['Hello file world!\n', 'Bye file world.\n'])
```

**Closing.** The file **close** method used earlier finalizes file contents and frees up system resources. For instance, closing forces buffered output data to be flushed out to disk. Normally, files are automatically closed when the file object is garbage collected by the interpreter (that is, when it is no longer referenced). This includes all remaining open files when the Python session or program exits. Because of that, **close** calls are often optional. In fact, it’s common to see file-processing code in Python in this idiom:

```python
open('somefile.txt', 'w').write("G'day Bruce\n") # write to temporary object
open('somefile.txt', 'r').read() # read from temporary object
```

Since both these expressions make a temporary file object, use it immediately, and do not save a reference to it, the file object is reclaimed right after data is transferred, and is automatically closed in the process. There is usually no need for such code to call the **close** method explicitly.

In some contexts, though, you may wish to explicitly close anyhow:

* For one, because the Jython implementation relies on Java’s garbage collector, you can’t always be as sure about when files will be reclaimed as you can in standard Python. If you run your Python code with Jython, you may need to close manually if many files are created in a short amount of time (e.g. in a loop), in order to avoid running out of file resources on operating systems where this matters.
* If you write to an output file in IDLE, be sure to explicitly close (or flush) your file if you need to reliably read it back during the same IDLE session.
* And while it seems very unlikely today, it’s not impossible that this auto-close on reclaim file feature could change in future.

For these reasons, manual close calls are not a bad idea in nontrivial programs, even if they are technically not required. Closing is a generally harmless but robust habit to form.

### Ensuring file closure: Exception handlers and context managers

If closure is required, though, there are two basic alternatives: the **try** statement’s **finally** clause is the most general, since it allows you to provide general exit actions for any type of exceptions:

```python
myfile = open(filename, 'w')
try:
    ...process myfile...
finally:
    myfile.close()
```

In recent Python releases, though, the **with** statement provides a more concise alterna- tive for some specific objects and exit actions, including closing files:

```python
with open(filename, 'w') as myfile:
    ...process myfile, auto-closed on statement exit...
```

In general terms, the 3.1 and later code:

```python
with A() as a, B() as b:
    ...statements...
```

Runs the same as the following, which works in 3.1, 3.0, and 2.6:

```python
with A() as a:
    with B() as b:
        ...statements...
```

For example, when the **with** statement block exits in the following, both files’ exit actions are automatically run to close the files, regardless of exception outcomes:

```python
with open('data') as fin, open('results', 'w') as fout:
    for line in fin:
        fout.write(transform(line))
```

### Input files

```python
C:\temp> python
>>> file = open('data.txt')     # open input file object: 'r' default
>>> lines = file.readlines()    # read into line string list
>>> for line in lines:          # BUT use file line iterator! (ahead)
... print(line, end='')         # lines have a '\n' at end
...
Hello file world!
Bye file world.
```

In fact, there are many ways to read an input file:

**file.read()**
> Returns a string containing all the characters (or bytes) stored in the file

**file.read(N)**
> Returns a string containing the next N characters (or bytes) from the file

**file.readline()**
> Reads through the next \n and returns a line string (contain \n)

**file.readlines()**
> Reads the entire file and returns a list of line strings

Let’s run these method calls to read files, lines, and characters from a text file—the **seek(0)** call is used here before each test to rewind the file to its beginning (more on this call in a moment):

```python
>>> file.seek(0)                        # go back to the front of file
>>> file.read()                         # read entire file into string
'Hello file world!\nBye file world.\n'

>>> file.seek(0)                        # read entire file into lines list
>>> file.readlines()
['Hello file world!\n', 'Bye file world.\n']

>>> file.seek(0)
>>> file.readline()                     # read one line at a time
'Hello file world!\n'
>>> file.readline()
'Bye file world.\n'
>>> file.readline()                     # empty string at end-of-file
''

>>> file.seek(0)                        # read N (or remaining) chars/bytes
>>> file.read(1), file.read(8)          # empty string at end-of-file
('H', 'ello fil')
```

All of these input methods let us be specific about how much to fetch. Here are a few rules of thumb about which to choose:
* **read()** and **readlines()** load the *entire file* into memory all at once. That makes them handy for grabbing a file’s contents with as little code as possible. It also makes them generally fast, but costly in terms of memory for huge files—loading a multigigabyte file into memory is not generally a good thing to do (and might not be possible at all on a given computer).
* On the other hand, because the **readline()** and **read(N)** calls fetch just *part of the file* (the next line or N-character-or-byte block), they are safer for potentially big files but a bit less convenient and sometimes slower. Both return an empty string when they reach end-of-file. If speed matters and your files aren’t huge, **read** or **readlines** may be a generally better choice.

### Reading lines with file iterators

In older versions of Python, the traditional way to read a file line by line in a **for** loop was to read the file into a list that could be stepped through as usual:

```python
>>> file = open('data.txt')
>>> for line in file.readlines(): # DON'T DO THIS ANYMORE!
...     print(line, end='')
```

In recent Pythons, the file object includes an *iterator* which is smart enough to grab just one line per request in all iteration con- texts, including **for** loops and list comprehensions. The practical benefit of this exten- sion is that you no longer need to call **readlines** in a **for** loop to scan line by line—the iterator reads lines on request automatically:

````python
>>> file = open('data.txt')
>>> for line in file:               # no need to call readlines
...     print(line, end='')         # iterator reads next line each time
...
Hello file world!
Bye file world.
````

Better still, you can open the file in the loop statement itself, as a temporary which will be automatically closed on garbage collection when the loop ends (that’s normally the file’s sole reference):

```python
>>> for line in open('data.txt'):   # even shorter: temporary file object
...     print(line, end='')         # auto-closed when garbage collected
...
Hello file world!
Bye file world.
```

If you want to see what really happens inside the **for** loop, you can use the iterator manually; it’s just a **__next__** method (run by the **next** built-in function), which is similar to calling the **readline** method each time through, except that read methods return an empty string at end-of-file (**EOF**) and the iterator raises an exception to end the iteration:

```python
>>> file = open('data.txt') # read methods: empty at EOF
>>> file.readline()
'Hello file world!\n'
>>> file.readline()
'Bye file world.\n'
>>> file.readline()
''

>>> file = open('data.txt') # iterators: exception at EOF
>>> file.__next__()         # no need to call iter(file) first,
'Hello file world!\n'       # since files are their own iterator
>>> file.__next__()
'Bye file world.\n'
>>> file.__next__()
Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
StopIteration
```

### Other open options

Besides the **w** and (default) **r** file open modes, most platforms support an a mode string, meaning “append.”

```python
>>> file = open('data.txt', 'a')    # open in append mode: doesn't erase
>>> file.write('The Life of Brian') # added at end of existing data
>>> file.close()
>>>
>>> open('data.txt').read()         # open and read entire file
'Hello file world!\nBye file world.\nThe Life of Brian'
```

## Binary and Text Files

```python
>>> file = open('data.txt', 'wb') # open binary output file
>>> file = open('data.txt', 'rb') # open binary input file
```

Continuing with our text file from preceding examples:

```python
>>> open('data.txt').read() # text mode: str
'Hello file world!\nBye file world.\nThe Life of Brian'

>>> open('data.txt', 'rb').read() # binary mode: bytes
b'Hello file world!\r\nBye file world.\r\nThe Life of Brian'

>>> file = open('data.txt', 'rb')
>>> for line in file: print(line)
...
b'Hello file world!\r\n'
b'Bye file world.\r\n'
b'The Life of Brian'
```

```python
>>> open('data.bin', 'wb').write(b'Spam\n')
5
>>> open('data.bin', 'rb').read()
b'Spam\n'

>>> open('data.bin', 'wb').write('spam\n')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: a bytes-like object is required, not 'str'
```

### Unicode encoding for text files

# Skip Binary and Text Files

## Lower-Level File Tools in the os Module

**os.open(*path*, *flags*, *mode*)**
> Opens a file and returns its descriptor

**os.read(*descriptor*, *N*)**
> Reads at most N bytes and returns a byte string

**os.write(*decriptor*, *string*)**
> Writes bytes in byte string ***string*** to the file

**os.lseek(*decripter*, *position*, *how*)**
> Moves to ***position*** in the file

### Using os.popen files

In fact, the **fileno** file object method returns the integer descriptor associated with a built-in file object.

```python
>>> import sys
>>> for stream in (sys.stdin, sys.stdout, sys.stderr):
... print(stream.fileno())
...
0
1
2

>>> sys.stdout.write('Hello stdio world\n')     # write via file method
Hello stdio world
18
>>> import os
>>> os.write(1, b'Hello descriptor world\n')    # write via os module
Hello descriptor world
23
```

```python
>>> file = open(r'C:\temp\spam.txt', 'w')       # create external file, object
>>> file.write('Hello stdio file\n')            # write via file object method
>>> file.flush()                                # else os.write to disk first!
>>> fd = file.fileno()                          # get descriptor from object
>>> fd
3
>>> import os
>>> os.write(fd, b'Hello descriptor file\n')    # write via os module
>>> file.close()
```

```shell script
C:\temp> type spam.txt                          # lines from both schemes
Hello stdio file
Hello descriptor file
```

### os.open module flags

```shell script
>>> fdfile = os.open(r'C:\temp\spam.txt', (os.O_RDWR | os.O_BINARY))
>>> os.read(fdfile, 20)
b'Hello stdio file\r\nHe'

>>> os.lseek(fdfile, 0, 0)    # go back to start of file
>>> os.read(fdfile, 100)      # binary mode retains "\r\n"
b'Hello stdio file\r\nHello descriptor file\n'

>>> os.lseek(fdfile, 0, 0)
>>> os.write(fdfile, b'HELLO') # overwrite first 5 bytes
5
```

````shell script
C:\temp> type spam.txt
HELLO stdio file
Hello descriptor file
````

# Directory Tools

## Walking One Directory

### Running shell listing commands with os.popen

### The glob module

````shell script
>>> import glob
>>> glob.glob('*')
['parts', 'PP3E', 'random.bin', 'spam.txt', 'temp.bin', 'temp.txt']

>>> glob.glob('*.bin')
['random.bin', 'temp.bin']

>>> glob.glob('parts')
['parts']

>>> glob.glob('parts/*')
['parts\\part0001', 'parts\\part0002', 'parts\\part0003', 'parts\\part0004']

>>> glob.glob('parts\part*')
['parts\\part0001', 'parts\\part0002', 'parts\\part0003', 'parts\\part0004']
````

### The os.listdir call

## Walking Directory Trees

### The os.walk visitor


