import unittest

from callbacks import supports_callbacks

class TestClassLevel(unittest.TestCase):
    def test_registries_are_separate(self):

        def callback():
            pass
        class ExampleClass(object):
            @supports_callbacks
            def method(self):
                pass

        e = ExampleClass()
        self.assertEquals(e.method.num_callbacks, (0,0))

        ExampleClass.method.add_callback(callback, label='foo')
        self.assertEquals(e.method.num_callbacks, (1, 0))

        e.method.add_callback(callback, label='foo')
        self.assertEquals(e.method.num_callbacks, (1, 1))

        e.method.remove_callback(label='foo')
        self.assertEquals(e.method.num_callbacks, (1, 0))

    def test_class_level_callbacks_fire_on_instances(self):
        called_with = []
        def callback(value):
            called_with.append(value)

        class ExampleClass(object):
            @supports_callbacks
            def method(self, value):
                pass

        # registered before instance is created
        ExampleClass.method.add_callback(callback, takes_target_args=True)
        self.assertEquals(ExampleClass.method.num_callbacks, 1)

        e = ExampleClass()
        self.assertEquals(e.method.num_callbacks, (1, 0))

        e.method(1234)
        self.assertEquals(called_with, [1234])

    def test_instance_level_callbacks_do_NOT_fire_on_other_instances(self):
        called_with = []
        def callback(value):
            called_with.append(value)

        class ExampleClass(object):
            @supports_callbacks
            def method(self, value):
                pass

        a = ExampleClass()
        b = ExampleClass()

        a.method.add_callback(callback, takes_target_args=True)
        self.assertEquals(a.method.num_callbacks, (0, 1))
        self.assertEquals(b.method.num_callbacks, (0, 0))

        a.method(1234)
        self.assertEquals(called_with, [1234])

        b.method(4321)
        self.assertEquals(called_with, [1234])
