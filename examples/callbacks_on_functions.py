from __future__ import absolute_import
from __future__ import print_function

from callbacks import supports_callbacks

def callback():
    print("Polly!")

@supports_callbacks
def target():
    print("hello", end=" ")

target.add_callback(callback)

print ("This should print 'hello Polly!':")
target() # prints "hello Polly!"
