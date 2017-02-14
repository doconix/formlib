#  Written by Conan Albrecht
#  Version: 0.1.3
#  Released under the Apache open source license
#

from django.conf import settings
from django import forms
from django_mako_plus import view_function
from . import dmp_render_to_string
import inspect


class FormMixIn(object):
    """
    A mixin that adds to the Django form class:

        - as_full() prints the full set of <form> tags, including the
          csrf token (see templates/form.htm).
        - Automatically adds the POST data if method is post.
        - Calls init(...) at the end of the __init__ process with
          any kwargs specified in init().
        - Adds a commit(...) method to keep form action with the form
          code.
        - Adds the request object to the form.

    Template:

        from django_mako_plus import view_function
        from formlib.form import FormMixIn
        from django import forms

        @view_function
        def process_request(request):

            # process the form
            form = MyForm(request, a=1, b=2)
            if form.is_valid():
                d = form.commit(c=3)
                return HttpResponseRedirect('/app/successurl/')

            # render the template
            return dmp_render(request, 'contact.html', {
                'form': form,
            })


        class MyForm(FormMixIn, forms.Form):
            '''An example form'''
            def init(self, a, b):
                '''Initialize the form (called at end of __init__)'''
                # do something with variables "a" and "b"
                print(a)
                print(b)
                # add fields here
                self.fields['name'] = forms.CharField()

            def commit(self, c):
                '''Process the form action'''
                # do something with c (optional)
                print(c)
                # act on the form
                print('Name is', self.cleaned_data['name'])
                # return any data (optional)
                return 4

    On your template:

        ${ form }

    """
    form_action = None
    form_method = 'POST'
    form_submit = 'Submit'
    field_css = [ 'form-control' ]

    def __init__(self, request, *args, **kwargs):
        '''Constructor'''
        # save the request object
        self.request = request

        # strip off the init() arguments
        init_kwargs = { k: kwargs.pop(k, None) for k in inspect.getargspec(self.init).args if k != 'self' }

        # check that the init_kwargs don't conflict with parameters of any superclass constructors
        if settings.DEBUG:
            mro_args = set()
            for klass in self.__class__.__mro__:
                mro_args.update(inspect.getargspec(klass.__init__).args)
            conflicts = mro_args & set(init_kwargs.keys())
            assert len(conflicts) == 0, '{}.init() arguments "{}" have the same name as __init__ arguments in its inheritance mro.  Please use another argument name.'.format(self.__class__.__qualname__, ', '.join(conflicts))

        # default POST and FILES if method is POST and they weren't provided
        # this gets the values from args, then kwargs, then, if post method, request.POST/FILES
        newargs = [
            args[0] if len(args) > 0 else kwargs.pop('data') if 'data' in kwargs else request.POST if request.method == 'POST' else None,
            args[1] if len(args) > 1 else kwargs.pop('files') if 'files' in kwargs else request.FILES if request.method == 'POST' else None,
        ]
        # add any additional args
        if len(args) > 2:
            newargs.extend(args[2:])

        # call superclass constructors
        super().__init__(*newargs, **kwargs)

        # call the init() as the last thing in the constructor
        self.init(**init_kwargs)


    def init(self):  # add any additional items to init()
        '''
        Called at the end of the constructor.
        Subclasses should override this method to set up the class.
        '''
        pass


    def as_full(self):
        '''Returns the HTML for this form, including <form>, submit, and csrf tags.'''
        # add the bootstrap css
        css = set(self.field_css)
        for field in self.fields.values():
            current = set(( c.strip() for c in field.widget.attrs.get('class', '').split(' ') if c ))
            field.widget.attrs['class'] = ' '.join(css | current)

        # render the string
        return dmp_render_to_string(self.request, 'form.htm', { 'form': self })


    def __str__(self):
        '''Returns the HTML for this form, including <form>, submit, and csrf tags.'''
        return self.as_full()


    def commit(self, *args, **kwargs):
        '''
        Commits the form after it has been validated.
        '''
        pass


