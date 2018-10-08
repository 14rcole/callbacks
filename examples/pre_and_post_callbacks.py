from __future__ import absolute_import
from __future__ import print_function

from callbacks import supports_callbacks

def pre_callback():
    print("Hello,", end=" ")

def post_callback():
    print("Do you want a cracker?")

@supports_callbacks
def print_string(string):
    print(string, end=" ")

print_string.add_post_callback(post_callback)
print_string.add_pre_callback(pre_callback)

print "This should print 'Hello, Polly! Do you want a cracker?':"
print_string('Polly!')
