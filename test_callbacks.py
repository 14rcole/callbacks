import unittest
import uuid

from callbacks import supports_callbacks

class TestOnMethod(unittest.TestCase):
    def callback(self, *args, **kwargs):
            self.called_with.append((args, kwargs))

    @supports_callbacks
    def target(self, *args, **kwargs):
        return (args, kwargs)

    def setUp(self):
        self.called_with = []
        self.target.remove_callbacks()

    def test_method_with_defaults(self):
        result = self.target(10, 20, key='value')
        self.assertEquals(result, ((10, 20), {'key':'value'}))
        self.assertEquals(len(self.called_with), 0)

        self.target.add_callback(self.callback)

        result = self.target(10, 20, key='value')
        self.assertEquals(result, ((10, 20), {'key':'value'}))
        self.assertEquals(len(self.called_with), 1)
        self.assertEquals(self.called_with[0], (tuple(), {}))

        result = self.target(30, 40, key='another_value')
        self.assertEquals(result, ((30, 40), {'key':'another_value'}))
        self.assertEquals(len(self.called_with), 2)
        self.assertEquals(self.called_with[1], (tuple(), {}))


called_with = []
def callback(*args, **kwargs):
    called_with.append((args, kwargs))

@supports_callbacks
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

