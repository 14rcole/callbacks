from callbacks import supports_callbacks

#     The class-level callbacks are called as the
# 'target' of the instance-level callbacks so the order cannot be made
# entirely arbitrary, the order is essentially:
#
#     INSTANCE_level_PRE_callbacks
#     try:
#         CLASS_level_PRE_callbacks
#         try:
#             original_target
#         except:
#             CLASS_level_EXCEPTION_callbacks
#         CLASS_level_POST_callbacks
#     except:
#         INSTANCE_level_EXCEPTION_callbacks
#     INSTANCE_level_POST_callbacks

def callback():
    print "you're a pretty bird!"

class ExampleClass(object):
    @supports_callbacks
    def print_string(self, string):
        print string,

e = ExampleClass()
e.print_string.add_post_callback(callback)

print "This should print 'Hello, you're a pretty bird!':"
e.print_string('Hello,')


def class_level_callback():
    print "Polly!"
    print "I think",

ExampleClass.print_string.add_post_callback(class_level_callback)
print "This should print 'Hello Polly!' then 'I think you're a pretty bird!':"
e.print_string('Hello')

