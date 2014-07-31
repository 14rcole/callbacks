from types import MethodType
from collections import defaultdict
import uuid
import inspect

class BaseSupportsCallbacks(object):
    '''
        This decorator enables a function or a class/instance method to register
    callbacks.  Callbacks can be registered to be run before or after the
    target function (or after the target function raises an exception).
    See the docstring for add_*_callback for more information.
    '''
    def __init__(self, target, target_is_method=False):
        self._target_is_method = target_is_method
        self.target = target
        self._update_docstring(target)
        self._initialize()

    def __get__(self, obj, obj_type=None):
        return MethodType(self, obj, obj_type)

    def _update_docstring(self, target):
        method_or_function = {True:'method',
                              False:'function'}
        docstring = \
        '''
            %s%s
        %s

        This %s supports callbacks.
          %s.add_pre_callback(callback)          returns: label
          %s.add_post_callback(callback)         returns: label
          %s.add_exception_callback(callback)    returns: label
          %s.remove_callback(label)
        ''' % (target.__name__,
               inspect.formatargspec(*inspect.getargspec(target)),
               target.__doc__,
               method_or_function[self._target_is_method],
               target.__name__,
               target.__name__,
               target.__name__,
               target.__name__)

        self.__doc__ = docstring

    def _initialize(self):
        # these hold the order in which callbacks were added
        self._pre_callbacks = defaultdict(list)
        self._post_callbacks = defaultdict(list)
        self._exception_callbacks = defaultdict(list)
        # this holds the callback functions and how they should be called
        self.callbacks = defaultdict(dict)

        # alias
        self.add_callback = self.add_post_callback

    def add_post_callback(self, callback,
            priority=0,
            label=None,
            takes_target_args=False,
            takes_target_result=False):
        '''
            Registers the callback to be called after the target is called.
        Inputs:
            callback: The callback function that will be called after
                the target is called.
            priority: Number. Higher priority callbacks are run first,
                ties are broken by the order in which callbacks were added.
            label: A name to call this callback, must be unique (and hashable)
                or None, if non-unique a RuntimeError will be raised.
                If None, a unique label will be automatically generated.
                NOTE: Callbacks can be removed using their label.
                      (see remove_callback)
            takes_target_args: If True, callback function will be passed the
                arguments and keyword arguments that are supplied to the
                target function.
            takes_target_result: If True, callback will be passed, as
                its first argument, the value returned from calling the
                target function.
        Returns:
            label
        '''
        priority, label = self._add_callback(callback, priority, label,
                takes_target_args)
        self._post_callbacks[priority].append(label)
        self.callbacks[label]['takes_target_result'] = takes_target_result
        return label

    def add_exception_callback(self, callback,
            priority=0,
            label=None,
            takes_target_args=False,
            handles_exception=False):
        '''
            Registers the callback to be called after the target raises an
        exception.  Exception callbacks are called in priority order and can
        handle the exception if they register with <handles_exception>.
        Inputs:
            callback: The callback function that will be called after
                the target function raises an exception.
            priority: Number. Higher priority callbacks are run first,
                ties are broken by the order in which callbacks were added.
            label: A name to call this callback, must be unique (and hashable)
                or None, if non-unique a RuntimeError will be raised.
                If None, a unique label will be automatically generated.
                NOTE: Callbacks can be removed using their label.
                      (see remove_callback)
            takes_target_args: If True, callback function will be passed the
                arguments and keyword arguments that are supplied to the
                target function.
            handles_exception: If True, callback will be passed (as
                its first argument) the exception raised by the target function
                or a higher priority exception_callback which raised an
                exception.  If True, this function is responsible for
                handling the exception or reraising it!  NOTE: If True and
                the exception has already been handled, this callback will
                not be called.
        Returns:
            label
        '''
        priority, label = self._add_callback(callback, priority, label,
                takes_target_args)
        self._exception_callbacks[priority].append(label)
        self.callbacks[label]['handles_exception'] = handles_exception
        return label

    def add_pre_callback(self, callback,
            priority=0,
            label=None,
            takes_target_args=False):
        '''
        Registers the callback to be called before the target.
        Inputs:
            callback: The callback function that will be called before
                the target function is run.
            priority: Number. Higher priority callbacks are run first,
                ties are broken by the order in which callbacks were added.
            label: A name to call this callback, must be unique (and hashable)
                or None, if non-unique a RuntimeError will be raised.
                If None, a unique label will be automatically generated.
                NOTE: Callbacks can be removed using their label.
                      (see remove_callback)
            takes_target_args: If True, callback function will be passed the
                arguments and keyword arguments that are supplied to the
                target function.
        Returns:
            label
        '''
        priority, label = self._add_callback(callback, priority, label,
                takes_target_args)
        self._pre_callbacks[priority].append(label)
        return label

    def _add_callback(self, callback, priority, label, takes_target_args):
        try:
            priority = float(priority)
        except:
            raise ValueError('Priority could not be cast into a float.')

        if label is None:
            label = uuid.uuid4()

        if label in self.callbacks.keys():
            raise RuntimeError('Callback with label="%s" already registered.'
                    % label)

        self.callbacks[label]['function'] = callback
        self.callbacks[label]['priority'] = priority
        self.callbacks[label]['takes_target_args'] = takes_target_args

        return priority, label

    def remove_callback(self, label):
        '''
        Unregisters the callback from the target.
        Inputs:
            label: The name of the callback.  This was either supplied as a
                keyword argument to add_callback or was automatically generated
                and returned from add_callback. If label is not valid a
                RuntimeError is raised.
        Returns:
            None
        '''
        if label not in self.callbacks.keys():
            raise RuntimeError(
                    'No callback with label "%s" attached to function "%s"' %
                    (label, self.target.__name__))

        for index in [self._pre_callbacks, self._post_callbacks,
                self._exception_callbacks]:
            for priority in index.keys():
                if label in index[priority]:
                    index[priority].remove(label)

        del self.callbacks[label]

    def remove_callbacks(self, labels=None):
        '''
        Unregisters callback(s) from the target.
        Inputs:
            labels: A list of callback labels.  If empty, all callbacks will
                be removed.
        Returns:
            None
        '''
        if labels is not None:
            bad_labels = []
            for label in labels:
                try:
                    self.remove_callback(label)
                except RuntimeError:
                    bad_labels.append(label)
                    continue
            if bad_labels:
                raise RuntimeError(
                    'No callbacks with labels %s attached to function %s' %
                    (bad_labels, self.target.__name__))
        else:
            self._initialize()

    def __call__(self, *args, **kwargs):
        if self._target_is_method:
            cb_args = args[1:] # skip over 'self' arg
        else:
            cb_args = args

        self._call_pre_callbacks(*cb_args, **kwargs)
        try:
            target_result = self.target(*args, **kwargs)
        except Exception as e:
            target_result = self._call_exception_callbacks(e, *cb_args, **kwargs)
        self._call_post_callbacks(target_result, *cb_args, **kwargs)
        return target_result

    def _call_pre_callbacks(self, *args, **kwargs):
        for priority in sorted(self._pre_callbacks.keys(), reverse=True):
            for label in self._pre_callbacks[priority]:
                callback = self.callbacks[label]['function']
                takes_target_args = self.callbacks[label]['takes_target_args']
                if takes_target_args:
                    callback(*args, **kwargs)
                else:
                    callback()

    def _call_exception_callbacks(self, exception, *args, **kwargs):
        result = None
        for priority in sorted(self._exception_callbacks.keys(), reverse=True):
            for label in self._exception_callbacks[priority]:
                callback = self.callbacks[label]['function']
                takes_target_args = self.callbacks[label]['takes_target_args']
                handles_exception = self.callbacks[label]['handles_exception']

                if handles_exception and exception is None:
                    # exception has already been handled, only call callbacks
                    # that don't handle exceptions
                    continue

                if takes_target_args and handles_exception:
                    try:
                        result = callback(exception, *args, **kwargs)
                        exception = None
                    except Exception as exception:
                        continue
                elif handles_exception:
                    try:
                        result = callback(exception)
                        exception = None
                    except Exception as exception:
                        continue
                elif takes_target_args:
                    callback(*args, **kwargs)
                else:
                    callback()
        if exception is not None:
            raise exception
        else:
            return result

    def _call_post_callbacks(self, target_result, *args, **kwargs):
        for priority in sorted(self._post_callbacks.keys(), reverse=True):
            for label in self._post_callbacks[priority]:
                callback = self.callbacks[label]['function']
                takes_target_args = self.callbacks[label]['takes_target_args']
                takes_target_result = self.callbacks[label]['takes_target_result']
                if takes_target_args and takes_target_result:
                    callback(target_result, *args, **kwargs)
                elif takes_target_result:
                    callback(target_result)
                elif takes_target_args:
                    callback(*args, **kwargs)
                else:
                    callback()

class MethodSupportsCallbacks(BaseSupportsCallbacks):
    def __init__(self, target):
        BaseSupportsCallbacks.__init__(self, target, target_is_method=True)

class FunctionSupportsCallbacks(BaseSupportsCallbacks):
    def __init__(self, target):
        BaseSupportsCallbacks.__init__(self, target, target_is_method=False)

def supports_callbacks(target_is_method=False):
    """
        This is a decorator, it has one keyword argument 'target_is_method' that
    should be set to True if decorating a bound method instead of a
    function.

    Once a function/method is decorated, you can register callbacks:
        <target>.add_pre_callback(callback)        returns: label
        <target>.add_post_callback(callback)       returns: label
        <target>.add_exception_callback(callback)  returns: label
    where <target> is the function/method that was decorated.

    To remove a callback you use:
        <target>.remove_callback(label)

    To remove all callbacks use:
        <target>.remove_callbacks()
    """

    if callable(target_is_method):
        # this support bare @supports_callbacks syntax (no calling brackets)
        target = target_is_method
        return FunctionSupportsCallbacks(target)

    if target_is_method:
        return MethodSupportsCallbacks
    else:
        return FunctionSupportsCallbacks

def method_supports_callbacks(target):
    return MethodSupportsCallbacks(target)

def function_supports_callbacks(target):
    return FunctionSupportsCallbacks(target)

