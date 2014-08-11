from callbacks import supports_callbacks

def print_first():
    print "first"

def print_second():
    print "second"

@supports_callbacks
def without_priorities():
    pass

without_priorities.add_callback(print_second)
without_priorities.add_callback(print_first)
print "This should print 'second' then 'first':"
without_priorities()


@supports_callbacks
def with_priorities():
    pass

with_priorities.add_callback(print_second, priority=1.0)
with_priorities.add_callback(print_first, priority=1.1)
print "This should print 'first' then 'second':"
with_priorities()
