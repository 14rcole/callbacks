from callbacks import supports_callbacks

def callback():
    print "Polly!"

@supports_callbacks
def target():
    print "hello",

target.add_callback(callback)

print "This should print 'hello Polly!':"
target() # prints "hello Polly!"
