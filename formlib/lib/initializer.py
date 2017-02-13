#  Written by Conan Albrecht
#  Version: 0.1.1
#  Released under the Apache open source license
#
import inspect

class InitializerMixIn(object):
    '''
    A mixin class that calls the init() method as the last part of the constructor.
    This allows subclasses to add initialization code without overriding the
    regular __init__() method and having to call super().
    '''
    def __init__(self, *args, **kwargs):
        '''Constructor'''
        # strip off the init() arguments
        init_kwargs = { k: kwargs.pop(k, None) for k in inspect.getargspec(self.init).args if k != 'self' }

        # call the superclass constructor
        super().__init__(*args, **kwargs)

        # call the init() as the last thing in the constructor
        self.init(**init_kwargs)


    def init(self):  # add any additional items to init()
        '''
        Called at the end of the constructor.
        Subclasses should override this method to set up the class.
        '''
        pass

