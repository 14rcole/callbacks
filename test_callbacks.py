import unittest
import uuid

from callbacks import supports_callbacks

class TestCallbackDecorator(unittest.TestCase):
    def test_with_defaults(self):
        called_with = []
        def callback(*args, **kwargs):
            called_with.append((args, kwargs))

        @supports_callbacks
        def foo(bar, baz='bone'):
            return (bar, baz)

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
        called_with = []
        def callback(*args, **kwargs):
            called_with.append((args, kwargs))

        @supports_callbacks
        def foo(bar, baz='bone'):
            return (bar, baz)

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

    def test_with_takes_target_results(self):
        called_with = []
        def callback(*args, **kwargs):
            called_with.append((args, kwargs))

        @supports_callbacks
        def foo(bar, baz='bone'):
            return (bar, baz)

        result = foo(10, 20)
        self.assertEquals(result, (10, 20))
        self.assertEquals(len(called_with), 0)

        foo.add_callback(callback, takes_target_results=True)

        result = foo(10, 20)
        self.assertEquals(result, (10, 20))
        self.assertEquals(len(called_with), 1)
        self.assertEquals(called_with[0], (((10, 20), ), {}))

        result = foo(10, baz=20)
        self.assertEquals(result, (10, 20))
        self.assertEquals(len(called_with), 2)
        self.assertEquals(called_with[1], (((10, 20), ),  {}))

    def test_with_takes_target_results_and_args(self):
        called_with = []
        def callback(*args, **kwargs):
            called_with.append((args, kwargs))

        @supports_callbacks
        def foo(bar, baz='bone'):
            return (bar, baz)

        result = foo(10, 20)
        self.assertEquals(result, (10, 20))
        self.assertEquals(len(called_with), 0)

        foo.add_callback(callback, takes_target_results=True,
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
        called_with = []
        def callback(*args, **kwargs):
            called_with.append((args, kwargs))

        @supports_callbacks
        def foo(bar, baz='bone'):
            return (bar, baz)

        result = foo(10, 20)
        self.assertEquals(result, (10, 20))
        self.assertEquals(len(called_with), 0)

        foo.add_callback(callback, call_before=True)

        result = foo(10, 20)
        self.assertEquals(result, (10, 20))
        self.assertEquals(len(called_with), 1)
        self.assertEquals(called_with[0], (tuple(), {}))

        result = foo(10, baz=20)
        self.assertEquals(result, (10, 20))
        self.assertEquals(len(called_with), 2)
        self.assertEquals(called_with[1], (tuple(), {}))

    def test_before_with_target_args(self):
        called_with = []
        def callback(*args, **kwargs):
            called_with.append((args, kwargs))

        @supports_callbacks
        def foo(bar, baz='bone'):
            return (bar, baz)

        result = foo(10, 20)
        self.assertEquals(result, (10, 20))
        self.assertEquals(len(called_with), 0)

        foo.add_callback(callback, takes_target_args=True, call_before=True)

        result = foo(10, 20)
        self.assertEquals(result, (10, 20))
        self.assertEquals(len(called_with), 1)
        self.assertEquals(called_with[0], ((10, 20), {}))

        result = foo(10, baz=20)
        self.assertEquals(result, (10, 20))
        self.assertEquals(len(called_with), 2)
        self.assertEquals(called_with[1], ((10, ), {'baz':20}))

    def test_multiple_before(self):
        called_order = []
        def cb1(*args, **kwargs):
            called_order.append('cb1')
        def cb2(*args, **kwargs):
            called_order.append('cb2')
        def cb3(*args, **kwargs):
            called_order.append('cb3')

        @supports_callbacks
        def foo(bar, baz='bone'):
            return (bar, baz)

        result = foo(10, 20)
        self.assertEquals(result, (10, 20))
        self.assertEquals(len(called_order), 0)

        foo.add_callback(cb1, call_before=True)
        foo.add_callback(cb2, call_before=True)
        foo.add_callback(cb3, call_before=True)

        result = foo(10, 20)
        self.assertEquals(result, (10, 20))
        self.assertEquals(called_order, ['cb1','cb2','cb3'])

    def test_multiple_before_priority(self):
        called_order = []
        def cb1(*args, **kwargs):
            called_order.append('cb1')
        def cb2(*args, **kwargs):
            called_order.append('cb2')
        def cb3(*args, **kwargs):
            called_order.append('cb3')

        @supports_callbacks
        def foo(bar, baz='bone'):
            return (bar, baz)

        result = foo(10, 20)
        self.assertEquals(result, (10, 20))
        self.assertEquals(len(called_order), 0)

        foo.add_callback(cb1, call_before=True)
        foo.add_callback(cb2, priority=1, call_before=True)
        foo.add_callback(cb3, priority=1, call_before=True)

        result = foo(10, 20)
        self.assertEquals(result, (10, 20))
        self.assertEquals(called_order, ['cb2','cb3','cb1'])

    def test_multiple(self):
        called_order = []
        def cb1(*args, **kwargs):
            called_order.append('cb1')
        def cb2(*args, **kwargs):
            called_order.append('cb2')
        def cb3(*args, **kwargs):
            called_order.append('cb3')

        @supports_callbacks
        def foo(bar, baz='bone'):
            return (bar, baz)

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
        called_order = []
        def cb1(*args, **kwargs):
            called_order.append('cb1')
        def cb2(*args, **kwargs):
            called_order.append('cb2')
        def cb3(*args, **kwargs):
            called_order.append('cb3')

        @supports_callbacks
        def foo(bar, baz='bone'):
            return (bar, baz)

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
        called_order = []
        def cb1(*args, **kwargs):
            called_order.append('cb1')
        def cb2(*args, **kwargs):
            called_order.append('cb2')
        def cb3(*args, **kwargs):
            called_order.append('cb3')

        @supports_callbacks
        def foo(bar, baz='bone'):
            return (bar, baz)

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
        called_order = []
        def cb1(*args, **kwargs):
            called_order.append('cb1')
        def cb2(*args, **kwargs):
            called_order.append('cb2')
        def cb3(*args, **kwargs):
            called_order.append('cb3')

        @supports_callbacks
        def foo(bar, baz='bone'):
            return (bar, baz)

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
        called_order = []
        def cb1(*args, **kwargs):
            called_order.append('cb1')
        def cb2(*args, **kwargs):
            called_order.append('cb2')
        def cb3(*args, **kwargs):
            called_order.append('cb3')

        @supports_callbacks
        def foo(bar, baz='bone'):
            return (bar, baz)

        result = foo(10, 20)
        self.assertEquals(result, (10, 20))
        self.assertEquals(len(called_order), 0)

        l1 = foo.add_callback(cb1, label=1)
        l2 = foo.add_callback(cb2, call_before=True, label=2)
        l3 = foo.add_callback(cb3)

        self.assertEquals(l1, 1)
        self.assertEquals(l2, 2)
        self.assertEquals(type(l3), type(uuid.uuid4()))
        
