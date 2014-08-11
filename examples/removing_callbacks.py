from callbacks import supports_callbacks

def print_one():
    print "1"

def print_a():
    print "a"

def print_foo():
    print 'foo'

def print_bar():
    print 'bar'

@supports_callbacks
def target():
    pass

target.add_callback(print_one)
label_a = target.add_callback(print_a)
label_foo = target.add_callback(print_foo)
label_bar = target.add_callback(print_bar)

print "This should print '1', 'a', 'foo', then 'bar':"
target()

# remove a single callback
target.remove_callback(label_foo)
print "This should print '1', 'a', then 'bar':"
target()

# remove a list of callbacks
target.remove_callbacks(labels=[label_a, label_bar])
print "This should print '1':"
target()

# even if you forgot to save the label, you can remove all callbacks
target.remove_callbacks()
print "This should print nothing:"
target()
