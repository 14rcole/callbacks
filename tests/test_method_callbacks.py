from collections import defaultdict
import unittest
from mock import Mock

from callbacks import supports_callbacks

callback_called_with = []
def example_callback(*args, **kwargs):
    print "CALLBACK called with args=%s kwargs=%s" %\
                (str(args), str(kwargs))
    callback_called_with.append((args, kwargs))

class ExampleClass(object):
    def __init__(self):
        self.method_called_with = []

    @supports_callbacks
    def example_method(self, *args, **kwargs):
        print "METHOD called with args=%s kwargs=%s" %\
                (str(args), str(kwargs))
        self.method_called_with.append((args, kwargs))
        return


class TestOnMethod(unittest.TestCase):
    def setUp(self):
        while callback_called_with:
            callback_called_with.pop()
        self.example = ExampleClass()

    def test_method_with_defaults(self):
        e = self.example
        e.example_method(10, 20, key='value')
        self.assertEquals(len(callback_called_with), 0)
        self.assertEquals(len(e.method_called_with), 1)
        self.assertEquals(e.method_called_with[0],
                ((10, 20), {'key':'value'}))

        e.example_method.add_callback(example_callback)

        e.example_method(11, 21, key='another_value')
        self.assertEquals(len(callback_called_with), 1)
        self.assertEquals(len(e.method_called_with), 2)

        self.assertEquals(e.method_called_with[1],
                ((11, 21), {'key':'another_value'}))
        self.assertEquals(callback_called_with[0],
                (tuple(),{}))

    def test_method_with_takes_target_args(self):
        e = self.example
        e.example_method(10, 20, key='value')
        self.assertEquals(len(callback_called_with), 0)
        self.assertEquals(len(e.method_called_with), 1)
        self.assertEquals(e.method_called_with[0],
                ((10, 20), {'key':'value'}))

        e.example_method.add_callback(example_callback,
                takes_target_args=True)

        e.example_method(11, 21, key='another_value')
        self.assertEquals(len(callback_called_with), 1)
        self.assertEquals(len(e.method_called_with), 2)

        self.assertEquals(e.method_called_with[1],
                ((11, 21), {'key':'another_value'}))
        self.assertEquals(callback_called_with[0],
                ((11, 21), {'key':'another_value'}))

    def test_class_method(self):
        e = self.example

        e.example_method(1)

        expected_called_with = [((1,),{})]
        self.assertEquals(expected_called_with, e.method_called_with)
        self.assertEquals([], callback_called_with)

        ExampleClass.example_method.add_callback(example_callback,
                takes_target_args=True)
        e.example_method.add_callback(example_callback,
                takes_target_args=False)

        # registering callback on class does NOT make it run when an instance
        # method executes
        e.example_method(2)
        expected_called_with = [((1,),{}), ((2,),{})]
        self.assertEquals(expected_called_with, e.method_called_with)
        self.assertEquals([(tuple(),{})], callback_called_with)

        # calling the class method does NOT execute a callback registered on the
        # instance method
        m = Mock()
        ExampleClass.example_method(m, 3)
        expected_called_with = [((1,),{}), ((2,),{})]
        self.assertEquals(expected_called_with, e.method_called_with)
        self.assertEquals([(tuple(),{}), ((m, 3),{})], callback_called_with)
