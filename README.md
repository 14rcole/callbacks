Callbacks lets you use decorator syntax to set callbacks on methods or functions.

[![Build Status](https://secure.travis-ci.org/14rcole/callbacks.svg?branch=master)](https://travis-ci.org/14rcole/callbacks)
[![Coverage Status](https://coveralls.io/repos/github/14rcole/callbacks/badge.svg?branch=master)](https://coveralls.io/github/14rcole/callbacks?branch=master)

```python
from callbacks import supports_callbacks

def callback():
    print "Polly!"

@supports_callbacks
def target():
    print "hello",

target.add_callback(callback)

target() # prints "hello Polly!"
```
