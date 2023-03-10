# Helper for Maxi

All the Functions I could need multiple times

## Instructions

1. Install:

```
pip install helper-for-maxi
```

2. Import package:

```python
from helper import *
# You can replace * with what you need!
``` 

## Currently Implemented Classes / Functions

BetterInput()
```python
import helper
helper.BetterInput(text: str, end: str = None, delay: float = None)

OR

from helper import BetterInput
BetterInput(text: str, end: str = None, delay: float = None)

# Gets an input
# 
# Prints the given `text` letter by letter using the specified delay and gets an input() after
# 
# Parameters
# ----------
# text: str
#     The text that is printed letter by letter
# 
# end: Optional[str]
#     The text that is passed into the :func:`input()` statement. 
#     Be aware that this part is not printed letter by letter.
#     DEFAULT: None
# 
# delay: Optional[float]
#     Changes the time between each printed letter
#     DEFAULT: None
```

BetterPrint()
```python
import helper
helper.BetterPrint(text: str, delay: float = .1)

OR

from helper import BetterPrint
BetterPrint(text: str, delay: float = .1)

# Prints text
# 
# Prints the given text letter by letter to the command line using the specified delay
# 
# Parameters
# ----------
# text: str
#     The text that is printed letter by letter
# 
# delay: Optional[float]
#     Changes the time between each printed letter
#     DEFAULT: .1
```

Output()
```python
import helper
helper.Output(outputValue)

OR

from helper import Output
Output(outputValue)

# Outputs to stdout
# 
# Outputs the given `outputValue` to stdout and flushes the stream after
# 
# Parameters
# ----------
# outputValue: :class:`Any`
#     The value that's written to stdout
```

Terminal
```python
import helper
helper.Terminal._  # _ = subclass

OR

from helper import Terminal
Terminal._         # _ = subclass

# Functions & Stuff for the Windows Terminal
# 
# Contains classes and Functions to use for/in the Windows Terminal
# 
# Subclasses
# ----------
# color:
#     Manipulates the color of the Terminal
```