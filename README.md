Callbacks lets you use decorator syntax to set callbacks on methods or functions.

```python
from callbacks import supports_callbacks

def callback():
    print "hello",

@supports_callbacks
def target():
    print "Polly"

target.add_callback(callback)

target() # prints "hello Polly!"
```

[![Build Status](https://secure.travis-ci.org/davidlmorton/callbacks.png?branch=master)](https://travis-ci.org/davidlmorton/callbacks)
