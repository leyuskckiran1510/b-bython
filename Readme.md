# BBYTHON [ Better B-Bython]

```
Why BBYTHON not Bython?

-> Because this is valid BBYTHON and PYTHON dict but not in BYTHON.
my_dict = {"bbython":"works"}

-> Because this is valid  BBYTHON and PYTHON function but not in BYTHON.
def my_func(my_dict={"works":True}):
    print(my_dict.get("works))

-> Because you can have code-blocks like in C.
{
    a = 10
    print(f"outer code block {a=}")
    {
        a = 20
        print(f"inner code block {a=}")
    }print("after inner code block")
    print(f"outer code block {a=}")
}
```

### `Note: except for the source files, other documentations,install scripts ... are copied from Bython itself`

B-Bython is a Python preprosessor which translates curly brackets into indentation,
but it doesnot use regex like it's predecessor [B-Bython](https://github.com/mathialo/b-bython)

## Content of README:

- [Key features](#key-features)
- [Code example](#code-example)
- [Installation](#installation)
- [Quick intro](#quick-intro)
- [Structure of the repository](#structure-of-the-repository)

## Key features

- "Forget" about indentaition. You should still write beautiful code, but if you mess up with tabs/spaces, or copy one piece of code to another that uses a different indentation style, it won't break.

- Uses Python for interpretation, that means that all of your existing modules, like NumPy and Matplotlib still works.

- You don't have to worry about random curly braces in your code breaking the whole script,
  as it uses state machine insted of using regular-expression (Yes regEx are also state machine) direclty.So you can use it to replace you indentation with braces and newline with semi-colens.

## Code example

```python
def print_message(num_of_times) {
    my_dict={"a":"b"}
    for i in range(num_of_times) {
        print("B-Bython is more-awesome!",my_dict);
    }
}

if __name__ == "__main__" {
    print_message(10);
}
```

## Installation

[TODO installation]

You can install B-Bython directly from PyPI using pip (with or without `sudo -H`, depending on your Python installation):

```
$ sudo -H pip3 install b_bython
```

If you for some reason want to install it from the git repository you can use `git clone` and do a local install instead:

```
$ git clone https://github.com/mathialo/b-bython.git
$ cd b-bython
$ sudo -H pip3 install .
```

The git version is sometimes a tiny bit ahead of the PyPI version, but not significantly.

To uninstall, simply run

```
$ sudo pip3 uninstall b_bython
```

which will undo all the changes.

## Quick intro

B-Bython works by first translating B-Bython-files (suggested file ending: .bby) into Python-files, and then using Python to run them. You therefore need a working installation of Python for B-Bython to work.

To run a B-Bython program, simply type

```
$ b_bython source.bby arg1 arg2 ...
```

to run `source.bby` with arg1, arg2, ... as command line arguments. If you want more details on how to run B-Bython files (flags, etc), type

```
$ b_bython -h
```

to print the built-in help page. You can also consult the man page by typing

```
$ man b_bython
```

Bython also includes a translator from Python to B-Bython. This is found via the `py2by` command:

```
$ py2by test.py
```

This will create a B-Bython file called `test.bby`. A full explanation of `py2by`, is found by typing

```
$ py2by -h
```

or by consulting the man page:

```
$ man py2by
```

For a more in-depth intro, consult the [b-bython introduction](INTRODUCTION.md)

## Structure of the repository

At the moment, B-Bython is written in Python. The git repository is structured into 4 directories:

- `b_bython` contains a Python package containing the parser and other utilities used by the main script
- `etc` contains manual pages and other auxillary files
- `scripts` contains the runnable Python scripts, ie the ones run from the shell
- `testcases` contains a couple of sample \*.bby and \*.py files intended for testing the implementation
