import unittest

from callbacks import supports_callbacks

class TestOnMethod(unittest.TestCase):
    def callback(self, *args, **kwargs):
            self.called_with.append((args, kwargs))

    @supports_callbacks(target_is_method=True)
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

    def test_method_with_takes_target_args(self):
        self.target.add_callback(self.callback, takes_target_args=True)

        result = self.target(10, 20, key='value')
        self.assertEquals(result, ((10, 20), {'key':'value'}))
        self.assertEquals(len(self.called_with), 1)
        self.assertEquals(self.called_with[0], ((10, 20), {'key':'value'}))
