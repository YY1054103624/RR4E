# Forking Processes

After a fork operation, the original copy of the program is called the *parent* process, and the copy created by **os.fork** is called the *child* process. In general, parents can make any number of children, and children can create child processes of their own; all forked processes run independently and in parallel under the operating system’s control, and children may continue to run after their parent exits.

*Example 5-1. PP4E\System\Processes\fork1.py*

```python

```