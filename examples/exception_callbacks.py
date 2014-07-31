from callbacks import supports_callbacks

def handler(exception):
    print "I handled exception %s" % str(exception)

def reporter():
    print "I noticed an exception occured"

@supports_callbacks
def target():
    raise RuntimeError

target.add_exception_callback(handler, handles_exception=True)
print "This should print 'I handled exception' and not crash"
target()

print "This should print 'I noticed an exception occured' and then crash"
target.remove_callbacks()
target.add_exception_callback(reporter)
target()
