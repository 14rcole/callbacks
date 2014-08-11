from callbacks import supports_callbacks

def print_args(*args, **kwargs):
    print "I got args %s and kwargs %s" % (str(args), str(kwargs))

@supports_callbacks
def target(*args, **kwargs):
    return 5

target.add_callback(print_args, takes_target_args=True)
print "This should print 'I got args (1,2,3) and kwargs {'foo':'bar'}' then 'target returned 5':"
print "target returned %s" % target(1, 2, 3, foo='bar')

target.remove_callbacks()
target.add_callback(print_args, takes_target_result=True)
print "This should print 'I got args (5,) and kwargs {}' then 'target returned 5':"
print "target returned %s" % target(1, 2, 3, foo='bar')
