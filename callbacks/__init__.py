from .callbacks import supports_callbacks
from .callbacks import method_supports_callbacks
from .callbacks import function_supports_callbacks

__version__ = '0.1.3'

__doc__ = """
    This library allows you to place decorators on functions and methods that
enable them to register callbacks.  For example:

from callbacks import supports_callbacks

def callback():
    print "Polly!"

@supports_callbacks
def target():
    print "hello",

target.add_callback(callback)

target() # prints "hello Polly!"
"""
