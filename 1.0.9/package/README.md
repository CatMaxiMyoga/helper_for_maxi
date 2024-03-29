# Helper for Maxi

All the Functions I could need multiple times

## Instructions

1. Install:

```
pip install helper-for-maxi
```

2. Import package:

```py
from maximyoga import *
OR
import maximyoga
maximyoga.*
# You can replace * with what you need!
``` 

## Currently Implemented Classes / Functions / Submodules

appendClipboard()
```py
import maximyoga
maximyoga.appendClipboard(text: str)

OR

from maximyoga import appendClipboard
appendClipboard(text: str)

# copies text
#
# Copies / Appends the given text to the windows clipboard using the utf-8 encoding
#
# Parameters
# ----------
# text: str
#     The text that is copied / appended to the clipboard
```

betterColorInput()
```py
import maximyoga
maximyoga.betterColorInput(text: str, beforeColor: Optional[Terminal.color.foreground] = Terminal.color.RESET, delay: float = .01)

OR

from maximyoga import betterColorInput
betterColorInput(text: str, beforeColor: Optional[Terminal.color.foreground] = Terminal.color.RESET, delay: float = .01)

# Gets an input
# 
# Prints the given text letter by letter using the specified delay and gets an input() in cyan after
# 
# Parameters
# ----------
# text: Optional[str]
#     The text that is printed letter by letter
#     DEFAULT: None
# 
# beforeColor: Optional[Terminal.color.foreground]
#     The color to change back to after getting the input
#     DEFAULT: None
# 
# delay: Optional[float]
#     Changes the time between each printed letter
#     DEFAULT: .01
```

betterInput()
```py
import maximyoga
maximyoga.betterInput(text: str = "", delay: float = .01)

OR

from maximyoga import betterInput
betterInput(text: str = "", delay: float = .01)

# Gets an input
# 
# Prints the given text letter by letter using the specified delay and gets an input() after
# 
# Parameters
# ----------
# text: Optional[str]
#     The text that is printed letter by letter
#     DEFAULT: ""
# 
# delay: Optional[float]
#     Changes the time between each printed letter
#     DEFAULT: .01
```

betterPrint()
```py
import maximyoga
maximyoga.betterPrint(text: str, delay: float = .01)

OR

from maximyoga import betterPrint
betterPrint(text: str, delay: float = .01)

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
#     DEFAULT: .01
# 
# newLine: Optional[bool]
#     whether to add a new line at the end or not
#     DEFAULT: True
```

colorInput()
```py
import maximyoga
maximyoga.colorInput(text: str = "", beforeColor: Optional[Terminal.color.foreground] = Terminal.color.RESET)

OR

from maximyoga import colorInput
colorInput(text: str = "", beforeColor: Optional[Terminal.color.foreground] = Terminal.color.RESET)

# Gets an input
# 
# executes the input() function in cyan and changes the color back to beforeColor if given
# 
# Parameters
# ----------
# text: Optional[str]
#     The text that is printed before getting the input
#     DEFAULT: None
# beforeColor: Optional[Terminal.color.foreground]
#     The color that was used before (if u want it to change back)
#     DEFAULT: None
```

kdict()
```py
import maximyoga
x = maximyoga.kdict(dictionary)

OR

from maximyoga import kdict
x = kdict(dictionary)

# Like dict but accessible with x.key and x["key"]
#
# A class that creates a dict that is also accessible by using x.key, not just by using x["key"]
#
# How To Use
# ----------
# x = kdict({"key": value, ...})
# y = x.key
# print(y) # Output: value
#
# OR
#
# d = {"key": value, ...}
# x = kdict(d)
# y = x.key
# print(y) # Output: value
```

KWArgsHandler()
```py
import maximyoga
x = maximyoga.KWArgsHandler(kwargs, *args: Union[str | tuple(str, type, any)])

OR

from maximyoga import KWArgsHandler
x = KWArgsHandler(kwargs, *args: Union[str | tuple(str, type, any)])

# Handles allowed keywords and types for values in kwargs
#
# Makes sure the parsed `kwargs` only contain allowed keywords and the correct types of values for the corresponding keywords
#
# Parameters
# ----------
# kwargs: dict
#	The keyword arguments to be used
#	
# *allowedKeywords: Union[str, tuple(str, type, any)]
#	tuple:
#		0: str: the allowed keyword
#		1: type: the expected type of value (object for any)
#		2: any: the default value, if not given: None
#	str: the allowed keyword
```

outputStdout()
```py
import maximyoga
maximyoga.outputStdout(outputValue)

OR

from maximyoga import outputStdout
outputStdout(outputValue)

# Outputs to stdout
# 
# Outputs the given outputValue to stdout and flushes the stream after
# 
# Parameters
# ----------
# outputValue: Any
#     The value that's written to stdout
```

Terminal
```py
import maximyoga
maximyoga.Terminal._  # _ = submodule

OR

from maximyoga.Terminal import _ # _ = submodule

# Functions & Stuff for the Windows Terminal
# 
# Contains classes and Functions to use for/in the Windows Terminal
# 
# Subclasses
# ----------
# color:
#     returns escape sequences to manipulate the color of the Terminal when printed
```