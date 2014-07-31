Callbacks lets you use decorator syntax to set callbacks on methods or functions.

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

[![Build Status](https://secure.travis-ci.org/davidlmorton/callbacks.svg?branch=master)](https://travis-ci.org/davidlmorton/callbacks)
[![Coverage Status](https://img.shields.io/coveralls/davidlmorton/callbacks.svg)](https://coveralls.io/r/davidlmorton/callbacks)
