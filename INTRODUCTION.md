# An introduction to B-bython

This document gives a more thorough introduction to B-bython.

## Table of contents

- [0 - Installation](#0---installation)
- [1 - The basics](#1---the-basics)
  - [1.1 - Running your program](#11---running-your-program)
  - [1.2 - Keeping generated Python files](#12---keeping-generated-python-files)
  - [1.3 - Different Python versions](#13---different-python-versions)
- [2 - Differences from regular Python](#2---differences-from-regular-python)
  - [2.1 - Dictionaries](#21---dictionaries)
  - [2.2 - else if](#22---else-if)
- [3 - Imports](#3---imports)
  - [3.1 - Importing B-bython modules in B-bython code](#31---importing-bython-modules-in-bython-code)
  - [3.2 - Importing Python modules in B-bython code](#32---importing-python-modules-in-bython-code)
  - [3.3 - Importing B-bython modules in Python code](#33---importing-bython-modules-in-python-code)
- [4 - Python files](#4---python-files)
  - [4.1 - Formatting of resulting Python files](#41---formatting-of-resulting-python-files)
  - [4.2 - Translating Python to B-bython](#42---translating-python-to-bython)

# 0 - Installation

B-bython is available from PyPI, so a call to pip should do the trick:

```bash
$ sudo -H pip3 install b_bython
```

B-Bython should now be available from the shell.

# 1 - The basics

B-Bython is pretty much Python, but instead of using colons and indentation to create blocks of code, we instead use curly braces. A simple example of some B-bython code should make this clear:

```python
import numpy as np
import matplotlib.pyplot as plt

def plot_sine_wave(xmin=0, xmax=2*np.pi, points=100, filename=None) {
    xs = np.linspace(xmin, xmax, points)
    ys = np.sin(xs)

    plt.plot(xs, ys)

    if filename is not None {
        plt.savefig(filename)
    }

    plt.show()
}

if __name__ == "__main__" {
    plot_sine_wave()
}
```

Curly braces are used whenever colons and indentation would be used in regular Python, ie function/class definitions, loops, if-statements, ...

As you can see in the example above, importing modules from Python is no issue. All packages installed with your normal Python installation is available in B-bython as well.

## 1.1 - Running your program

Say we have written the above program, and saved it as `test.by`. To parse and run the program, use the `b_bython` command in the shell

```bash
b_bython test.by
```

A plot containing one period of a sine wave should appear.

## 1.2 - Keeping generated Python files

B-Bython works by first translating your B-bython files to regular Python, and then use Python to run it. After running, the created Python files are deleted. If you want to keep the created files after running, use the `-k` (k for 'keep') flag:

```bash
b_bython -k test.by
```

If you don't want the program to be run, but only translated to Python, use the `-c` flag (c for 'compile'):

```bash
b_bython -c test.by
```

In both cases, a file called `test.py` will remain in the directory you are working from.

If you want more control on the resulting outputfile, you can use the `-o` flag to specify the output file:

```bash
b_bython -c -o out/python_test.py test.by
```

## 1.3 - Different Python versions

B-Bython is written in Python 3, so you need a working installation of Python 3.x to run B-bython. Your B-bython files, however, can be run in whatever Python version you prefer. The standard is Python 3 (ie, B-bython will use the env command `python3` to run your program), but if you for legacy reasons want to run Python 2 instead, you can use the `-2` flag to do that:

```bash
b_bython -2 test.by
```

# 2 - Differences from regular Python

B-Bython is created to be as similar to Python as possible, but there are a few important differences.

## 2.1 - Dictionaries

You can use dictionaries as you whish no edge cases like in [Bython](https://raw.githubusercontent.com/mathialo/bython)

## 2.2 - else if

The standard way of creating if-chains in Python is with the `elif` keyword:

```python
if x > 5:
    print("value is bigger than 5")
elif x == 5:
    print("value is 5")
else:
    print("value is smaller than 5")
```

B-bython introduces C-style `else if` as an additional alternative. Normal `elif` is of course still valid:

```python
# Python-style 'elif':
if x > 5 {
    print("value is bigger than 5")
} elif x == 5 {
    print("value is 5")
} else {
    print("value is smaller than 5")
}

# C-style 'else if'
if x > 5 {
    print("value is bigger than 5")
} else if x == 5 {
    print("value is 5")
} else {
    print("value is smaller than 5")
}
```

Both are valid and will work.

# 3 - Imports

B-bython handles imports quite well. In this section we will look at the different scenarios where imports might occur.

## 3.1 - Importing B-bython modules in B-bython code

Importing B-bython into B-bython is not an issue at all. Before parsing the source file, B-bython will also look for imports and automatically parse them as well. Say we have these two b-bython files:

main.by:

```python
import test_module

test_module.func()
```

test_module.by:

```python
def func() {
    print("hello!")
}
```

When running

```bash
$ b_bython main.by
```

B-bython will detect that test_module is imported and look for a file named `test_module.by` and parse that as well. This will also handle additional imports from `test_module.by`, and so on. It will also avoid circular imports.

## 3.2 - Importing Python modules in B-bython code

As illustrated in the example in Section 1, B-bython will automatically work with any Python modules/packages you have installed.

Local imports from Python files in the same directory is no issue either.

## 3.3 - Importing B-bython modules in Python code

Importing B-bython code into Python is a bit more tricky, but still quite streamlined. To import B-bython modules in Python, you must use the `b_bython_import` function from the `b_bython.importing` module. Assume that the `test_module.by` file described in Section 3.1 is avaliable. To import it in a Python file, you can do as follows:

```python
from b_bython.importing import b_bython_import
bython_import("test_module", globals())

# The module is now available as test_module:
test_module.func()
```

# 4 - Python files

## 4.1 - Formatting of resulting Python files

B-bython doesnot tries to keep the line numbers in the resulting Python files equivalent to the ones in the original source file. Thus, if an error occurs on line 42 when running Python, you can go to line 42 in the B-bython code to inspect the error.
But if you write in a minimized version you might struggle to find error,
[TODO:improve error pointing]

However, this approach yields some undesirable formatting on the resulting Python code. You should therefore consider using some Python formatter like [yapf](https://github.com/google/yapf) or [black](https://github.com/ambv/black) on the output from B-bython to make the resulting Python code nice and tidy.

## 4.2 - Translating Python to B-bython

If you want to translate Python code to B-bython, you can use the built-in `py2by` script. It's an experimental feature, but seems to work quite well.
