import unittest

from callbacks import supports_callbacks

called_with = []
called_order = []

class foo_error(RuntimeError):
    def __eq__(self, other):
        return isinstance(other, self.__class__)

class c5_error(ValueError):
    def __eq__(self, other):
        return isinstance(other, self.__class__)

def c1():
    called_order.append('c1')

def c2(exception):
    called_with.append((exception,))
    called_order.append('c2')
    raise exception

def c3(*args, **kwargs):
    called_with.append((args, kwargs))
    called_order.append('c3')

def c4(exception, *args, **kwargs):
    called_with.append((exception, args, kwargs))
    called_order.append('c4')
    return 'c4 returned this'

def c5(exception, *args, **kwargs):
    called_with.append((exception, args, kwargs))
    called_order.append('c5')
    raise c5_error

@supports_callbacks
def foo(bar, baz='bone'):
    raise foo_error
    return (bar, baz)

class TestExceptions(unittest.TestCase):
    def setUp(self):
        while called_with:
            called_with.pop()
        while called_order:
            called_order.pop()
        foo.remove_callbacks()

    def test_c1(self):
        foo.add_exception_callback(c1)

        self.assertRaises(foo_error, foo, 1, baz=2)

        self.assertEqual(len(called_with), 0)

    def test_c2(self):
        foo.add_exception_callback(c2, handles_exception=True)

        self.assertRaises(foo_error, foo, 1, baz=2)

        self.assertEqual(len(called_with), 1)
        self.assertTrue(isinstance(called_with[0][0], foo_error))

    def test_c3(self):
        foo.add_exception_callback(c3, takes_target_args=True)

        self.assertRaises(foo_error, foo, 1, baz=2)

        self.assertEqual(len(called_with), 1)
        self.assertEqual(called_with[0][0], (1,))
        self.assertEqual(called_with[0][1], {'baz':2})

    def test_c2_and_3(self):
        foo.add_exception_callback(c2, handles_exception=True)
        foo.add_exception_callback(c3, takes_target_args=True)

        self.assertRaises(foo_error, foo, 1, baz=2)

        self.assertEqual(len(called_with), 2)
        self.assertTrue(isinstance(called_with[0][0], foo_error))
        self.assertEqual(called_with[1][0], (1,))
        self.assertEqual(called_with[1][1], {'baz':2})

    def test_c4(self):
        foo.add_exception_callback(c4, handles_exception=True,
                takes_target_args=True)

        result = foo(1, baz=2)

        self.assertEqual('c4 returned this', result)
        self.assertEqual(len(called_with), 1)
        expected_called_with = [
                (foo_error(), (1,), {'baz':2})
                ]
        self.assertEqual(expected_called_with, called_with)

    def test_c4_without_takes_args(self):
        foo.add_exception_callback(c4, handles_exception=True)

        result = foo(1, baz=2)

        self.assertEqual('c4 returned this', result)
        expected_called_with = [(foo_error(), tuple(), {})]
        self.assertEqual(expected_called_with, called_with)

    def test_c5(self):
        foo.add_exception_callback(c5, handles_exception=True)

        self.assertRaises(c5_error, foo, 1, baz=2)

        expected_called_with = [(foo_error(), tuple(), {})]
        self.assertEqual(expected_called_with, called_with)

    def test_c5_takes_target_args(self):
        foo.add_exception_callback(c5, takes_target_args=True, handles_exception=True)

        self.assertRaises(c5_error, foo, 1, baz=2)

        self.assertEqual(len(called_with), 1)
        expected_called_with = [(foo_error(), (1,), {'baz': 2})]
        self.assertEqual(expected_called_with, called_with)

    def test_c3_and_c4_and_c5(self):
        foo.add_exception_callback(c3, priority=0.1, takes_target_args=True)
        foo.add_exception_callback(c5, priority=0.2, handles_exception=True)
        foo.add_exception_callback(c4, priority=0.3, takes_target_args=True,
                handles_exception=True)

        result = foo(1, baz=2)

        self.assertEqual('c4 returned this', result)
        self.assertEqual(['c4', 'c3'], called_order)
        self.assertEqual(len(called_with), 2)
        expected_called_with = [
                (foo_error(), (1,), {'baz':2}),
                ((1,), {'baz':2}),
                ]
        self.assertEqual(expected_called_with, called_with)

    def test_pre_post1(self):
        foo.add_pre_callback(c3, takes_target_args=True)
        foo.add_post_callback(c3, takes_target_args=True)
        foo.add_exception_callback(c4, takes_target_args=True,
                handles_exception=True)

        result = foo(1, baz=2)

        self.assertEqual('c4 returned this', result)
        self.assertEqual(['c3', 'c4', 'c3'], called_order)
        self.assertEqual(len(called_with), 3)
        expected_called_with = [
                ((1,), {'baz':2}),
                (foo_error(), (1,), {'baz':2}),
                ((1,), {'baz':2}),
                ]
        self.assertEqual(expected_called_with, called_with)

    def test_pre_post2(self):
        foo.add_pre_callback(c3, takes_target_args=True)
        foo.add_post_callback(c3, takes_target_args=True)
        foo.add_exception_callback(c5, handles_exception=True)

        self.assertRaises(c5_error, foo, 1, baz=2)

        self.assertEqual(['c3', 'c5'], called_order)
        self.assertEqual(len(called_with), 2)
        expected_called_with = [((1,), {'baz': 2}), (foo_error(), (), {})]
        self.assertEqual(expected_called_with, called_with)


