import unittest
import uuid

from callbacks import supports_callbacks

called_with = []
def callback(*args, **kwargs):
    called_with.append((args, kwargs))

@supports_callbacks()
def foo(bar, baz='bone'):
    return (bar, baz)

called_order = []
def cb1(*args, **kwargs):
    called_order.append('cb1')
def cb2(*args, **kwargs):
    called_order.append('cb2')
def cb3(*args, **kwargs):
    called_order.append('cb3')

class TestCallbackDecorator(unittest.TestCase):
    def setUp(self):
        while called_with:
            called_with.pop()
        while called_order:
            called_order.pop()
        foo.remove_callbacks()

    def test_with_defaults(self):
        result = foo(10, 20)
        self.assertEquals(result, (10, 20))
        self.assertEquals(len(called_with), 0)

        foo.add_callback(callback)

        result = foo(10, 20)
        self.assertEquals(result, (10, 20))
        self.assertEquals(len(called_with), 1)
        self.assertEquals(called_with[0], (tuple(), {}))

        result = foo(10, baz=20)
        self.assertEquals(result, (10, 20))
        self.assertEquals(len(called_with), 2)
        self.assertEquals(called_with[1], (tuple(), {}))

    def test_raises(self):
        self.assertRaises(ValueError, foo.add_callback, callback, priority='boo')

    def test_duplicate_label(self):
        foo.add_callback(callback, label='a')
        self.assertRaises(RuntimeError, foo.add_callback, callback, label='a')

    def test_remove_raises(self):
        foo.add_callback(callback)
        foo.add_callback(callback, label='good_label')

        self.assertRaises(RuntimeError, foo.remove_callback, 'bad_label')
        self.assertRaises(RuntimeError, foo.remove_callbacks, ['bad_label', 'good_label'])
        self.assertEqual(len(foo.callbacks), 1)

    def test_callbacks_info(self):
        foo.add_pre_callback(callback, label='a')
        foo.add_pre_callback(callback, label='b', takes_target_args=True)
        foo.add_post_callback(callback, label='c', priority=1.1,
                takes_target_result=True)
        foo.add_exception_callback(callback, label='d')
        expected_string =\
'''                                 Label   priority   order        type   takes args    takes result
                                     a        0.0       0         pre        False             N/A
                                     b        0.0       1         pre         True             N/A
                                     c        1.1       0        post        False            True
                                     d        0.0       0   exception        False             N/A'''
        self.assertEquals(expected_string, foo._callbacks_info)

    def test_with_takes_target_args(self):
        result = foo(10, 20)
        self.assertEquals(result, (10, 20))
        self.assertEquals(len(called_with), 0)

        foo.add_callback(callback, takes_target_args=True)

        result = foo(10, 20)
        self.assertEquals(result, (10, 20))
        self.assertEquals(len(called_with), 1)
        self.assertEquals(called_with[0], ((10, 20), {}))

        result = foo(10, baz=20)
        self.assertEquals(result, (10, 20))
        self.assertEquals(len(called_with), 2)
        self.assertEquals(called_with[1], ((10, ), {'baz':20}))

    def test_with_takes_target_result(self):
        result = foo(10, 20)
        self.assertEquals(result, (10, 20))
        self.assertEquals(len(called_with), 0)

        foo.add_callback(callback, takes_target_result=True)

        result = foo(10, 20)
        self.assertEquals(result, (10, 20))
        self.assertEquals(len(called_with), 1)
        self.assertEquals(called_with[0], (((10, 20), ), {}))

        result = foo(10, baz=20)
        self.assertEquals(result, (10, 20))
        self.assertEquals(len(called_with), 2)
        self.assertEquals(called_with[1], (((10, 20), ),  {}))

    def test_with_takes_target_result_and_args(self):
        result = foo(10, 20)
        self.assertEquals(result, (10, 20))
        self.assertEquals(len(called_with), 0)

        foo.add_callback(callback, takes_target_result=True,
                takes_target_args=True)

        result = foo(10, 20)
        self.assertEquals(result, (10, 20))
        self.assertEquals(len(called_with), 1)
        self.assertEquals(called_with[0], (((10, 20), 10, 20), {}))

        result = foo(10, baz=20)
        self.assertEquals(result, (10, 20))
        self.assertEquals(len(called_with), 2)
        self.assertEquals(called_with[1], (((10, 20), 10),  {'baz':20}))

    def test_before(self):
        result = foo(10, 20)
        self.assertEquals(result, (10, 20))
        self.assertEquals(len(called_with), 0)

        foo.add_pre_callback(callback)

        result = foo(10, 20)
        self.assertEquals(result, (10, 20))
        self.assertEquals(len(called_with), 1)
        self.assertEquals(called_with[0], (tuple(), {}))

        result = foo(10, baz=20)
        self.assertEquals(result, (10, 20))
        self.assertEquals(len(called_with), 2)
        self.assertEquals(called_with[1], (tuple(), {}))

    def test_before_with_target_args(self):
        result = foo(10, 20)
        self.assertEquals(result, (10, 20))
        self.assertEquals(len(called_with), 0)

        foo.add_pre_callback(callback, takes_target_args=True)

        result = foo(10, 20)
        self.assertEquals(result, (10, 20))
        self.assertEquals(len(called_with), 1)
        self.assertEquals(called_with[0], ((10, 20), {}))

        result = foo(10, baz=20)
        self.assertEquals(result, (10, 20))
        self.assertEquals(len(called_with), 2)
        self.assertEquals(called_with[1], ((10, ), {'baz':20}))

    def test_multiple_before(self):
        result = foo(10, 20)
        self.assertEquals(result, (10, 20))
        self.assertEquals(len(called_order), 0)

        foo.add_pre_callback(cb1)
        foo.add_pre_callback(cb2)
        foo.add_pre_callback(cb3)

        result = foo(10, 20)
        self.assertEquals(result, (10, 20))
        self.assertEquals(called_order, ['cb1','cb2','cb3'])

    def test_multiple_before_priority(self):
        result = foo(10, 20)
        self.assertEquals(result, (10, 20))
        self.assertEquals(len(called_order), 0)

        foo.add_pre_callback(cb1)
        foo.add_pre_callback(cb2, priority=1)
        foo.add_pre_callback(cb3, priority=1)

        result = foo(10, 20)
        self.assertEquals(result, (10, 20))
        self.assertEquals(called_order, ['cb2','cb3','cb1'])

    def test_multiple(self):
        result = foo(10, 20)
        self.assertEquals(result, (10, 20))
        self.assertEquals(len(called_order), 0)

        foo.add_callback(cb1)
        foo.add_callback(cb2)
        foo.add_callback(cb3)

        result = foo(10, 20)
        self.assertEquals(result, (10, 20))
        self.assertEquals(called_order, ['cb1','cb2','cb3'])

    def test_multiple_priority(self):
        result = foo(10, 20)
        self.assertEquals(result, (10, 20))
        self.assertEquals(len(called_order), 0)

        foo.add_callback(cb1)
        foo.add_callback(cb2, priority=1)
        foo.add_callback(cb3, priority=1)

        result = foo(10, 20)
        self.assertEquals(result, (10, 20))
        self.assertEquals(called_order, ['cb2','cb3','cb1'])

    def test_remove_callback(self):
        result = foo(10, 20)
        self.assertEquals(result, (10, 20))
        self.assertEquals(len(called_order), 0)

        foo.add_callback(cb1)
        label = foo.add_callback(cb2)
        foo.add_callback(cb3)

        result = foo(10, 20)
        self.assertEquals(result, (10, 20))
        self.assertEquals(called_order, ['cb1','cb2','cb3'])

        foo.remove_callback(label)

        result = foo(10, 20)
        self.assertEquals(result, (10, 20))
        self.assertEquals(called_order, ['cb1','cb2','cb3', 'cb1', 'cb3'])

    def test_remove_callbacks(self):
        result = foo(10, 20)
        self.assertEquals(result, (10, 20))
        self.assertEquals(len(called_order), 0)

        l1 = foo.add_callback(cb1)
        l2 = foo.add_callback(cb2)
        foo.add_callback(cb3)

        result = foo(10, 20)
        self.assertEquals(result, (10, 20))
        self.assertEquals(called_order, ['cb1','cb2','cb3'])

        foo.remove_callbacks([l1, l2])

        result = foo(10, 20)
        self.assertEquals(result, (10, 20))
        self.assertEquals(called_order, ['cb1','cb2','cb3', 'cb3'])

        foo.remove_callbacks()

        result = foo(10, 20)
        self.assertEquals(result, (10, 20))
        self.assertEquals(called_order, ['cb1','cb2','cb3', 'cb3'])

    def test_labels(self):
        result = foo(10, 20)
        self.assertEquals(result, (10, 20))
        self.assertEquals(len(called_order), 0)

        l1 = foo.add_callback(cb1, label=1)
        l2 = foo.add_pre_callback(cb2, label=2)
        l3 = foo.add_callback(cb3)

        self.assertEquals(l1, 1)
        self.assertEquals(l2, 2)
        self.assertEquals(type(l3), type(uuid.uuid4()))

