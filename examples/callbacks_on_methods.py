from callbacks import supports_callbacks

def callback():
    print "you're a pretty bird!"

class ExampleClass(object):
    @supports_callbacks
    def print_string(self, string):
        print string,

e = ExampleClass()
e.print_string.add_callback(callback)

print "This should print 'Hello, you're a pretty bird!':"
e.print_string('Hello,')
