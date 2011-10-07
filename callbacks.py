from types import MethodType, FunctionType
from functools import update_wrapper
from collections import defaultdict
import uuid
import inspect

class supports_callbacks(object):
    '''
        This decorator turns a function or a class method into a function which
    is able to register callbacks.  Callbacks can be registered to be run
    before and/or after the target function.  See the docstring for
    add_callback for more information.
    '''
    def __init__(self, target):
        self.target = target
        self._update_docstring(target)
        self._pre_callbacks = defaultdict(list)
        self._post_callbacks = defaultdict(list)
        self._callback_functions = {} 
        self._takes_target_args_status = {}
        self._takes_target_results_status = {}

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
          %s.add_callback(callback)    returns: label
          %s.remove_callback(label)
        ''' % ( target.__name__,
                inspect.formatargspec(*inspect.getargspec(target)),
                target.__doc__,
                method_or_function[inspect.ismethod(target)],
                target.__name__,
                target.__name__)

        self.__doc__ = docstring

    @property
    def callbacks(self):
        return self._callback_functions

    def add_callback(self, callback, 
            priority=0, 
            label=None,
            takes_target_args=False, 
            takes_target_results=False, 
            call_before=False):
        '''
        Registers the callback to be called after* the target.
        Inputs:
            callback: The callback function that will be called after*
                the target function is run.
            priority: Higher priority callbacks are run first,
                ties are broken by the order in which callbacks were added.
            label: A name to call this callback, must be unique (and hashable)
                or None, if non-unique it will raise a RuntimeError.
                If None, a unique label will be automatically generated.
                NOTE: Callbacks can be removed using their label. 
                      (see remove_callback)
            takes_target_args: If True, callback function will accept the 
                arguments and keyword arguments that are supplied to the 
                target function.
            takes_target_results: If True, callback will accept as its first 
                argument the results of the target function.
            *call_before: If True, the callback function will be called
                before the target function.  If True, the take_target_results 
                argument is ignored.
        Returns:
            label
        '''
        try:
            priority = int(priority)
        except:
            raise RuntimeError('Priority could not be cast into an integer.')

        if label is None:
            label = uuid.uuid4()

        if label in self._callback_functions.keys():
            raise RuntimeError('Callback with label="%s" already registered.' 
                    % label)
        else:
            self._callback_functions[label] = callback

        if call_before:
            self._pre_callbacks[priority].append(label)
        else:
            self._post_callbacks[priority].append(label)

        self._takes_target_args_status[label] = takes_target_args
        self._takes_target_results_status[label] = takes_target_results
        return label

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
        if label not in self._callback_functions.keys():
            raise RuntimeError(
                    'No callback with label "%s" attached to function "%s"' % 
                    (label, self.f.__name__))

        for priority in self._pre_callbacks.keys():
            if label in self._pre_callbacks[priority]:
                self._pre_callbacks[priority].remove(label)

        for priority in self._post_callbacks.keys():
            if label in self._post_callbacks[priority]:
                self._post_callbacks[priority].remove(label)

        del self._takes_target_args_status[label]
        del self._takes_target_results_status[label]
        del self._callback_functions[label]

    def remove_callbacks(self, labels=[]):
        '''
        Unregisters callback(s) from the target.
        Inputs:
            labels: A list of callback labels.  If empty, all callbacks will
                be removed.
        Returns:
            None
        '''
        if labels:
            bad_labels = []
            for label in labels:
                try:
                    self.remove_callback(label)
                except RuntimeError:
                    bad_labels.append(label)
                    continue
            if bad_labels:
                raise RuntimeError(
                    'No callbacks with labels "%s" attached to function %s' % 
                    (bad_labels, self.f.__name__))
        else:
            self._pre_callbacks = defaultdict(list)
            self._post_callbacks = defaultdict(list)
            self._callback_functions = {} 
            self._takes_target_args_status = {}
            self._takes_target_results_status = {}

    def __call__(self, *args, **kwargs):
        if inspect.ismethod(self.target):
            cb_args = args[1:] # skip over 'self' arg
        else:
            cb_args = args

        self._call_pre_callbacks(*cb_args, **kwargs)
        target_result = self.target(*args, **kwargs)
        self._call_post_callbacks(target_result, *cb_args, **kwargs)

        return target_result

    def _call_pre_callbacks(self, *args, **kwargs):
        for priority in reversed(sorted(self._pre_callbacks.keys())):
            for label in self._pre_callbacks[priority]:
                if self._takes_target_args_status[label]:
                    self._callback_functions[label](*args, **kwargs)
                else:
                    self._callback_functions[label]()

    def _call_post_callbacks(self, target_result, *args, **kwargs):
        for priority in reversed(sorted(self._post_callbacks.keys())):
            for label in self._post_callbacks[priority]:
                takes_args = self._takes_target_args_status[label]
                takes_results = self._takes_target_results_status[label]
                if takes_args and takes_results:
                    self._callback_functions[label](target_result, 
                            *args, **kwargs)
                elif takes_results:
                    self._callback_functions[label](target_result)
                elif takes_args:
                    self._callback_functions[label](*args, **kwargs)
                else:
                    self._callback_functions[label]()
