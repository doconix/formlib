#  Written by Conan Albrecht
#  Version: 0.1.5
#  Released under the Apache open source license
#

from django.conf import settings
from django import forms
from django_mako_plus import view_function, render_template
from inspect import Signature
import inspect


formsig = Signature.from_callable(forms.Form.__init__)


class Formless(forms.Form):
    """
    A mixin that prints a full form (instead of just the fields).

    In your view.py file:

        from django.http import HttpResponseRedirect
        from django_mako_plus import view_function
        from formlib import Formless
        from django import forms

        @view_function
        def process_request(request, user:amod.User=None):

            # process the form
            form = MyForm(request, user=user)
            if form.is_valid():
                form.commit()
                return HttpResponseRedirect('/app/successurl/')

            # render the template
            return request.dmp_render('mytemplate.html', {
                'form': form,
            })


        class MyForm(formlib.Form):   # extending formlib.Form, not Django's forms.Form
            '''An example form'''
            def init(self):
                '''Adds the fields for this form (called at end of __init__)'''
                # note that self.user is available (see MyForm constructor call above)
                self.initial = { 'name': self.user.first_name' }
                self.fields['name'] = forms.CharField()

            def clean_name(self):
                name = self.cleaned_data.get('name')
                # ...
                return name

            def commit(self):
                '''Process the form action'''
                # self.user still available
                self.user.first_name = self.cleaned_data.get('name')
                self.user.save()

    In your template.html file:

        ${ form }

    """
    form_id = 'form'
    form_action = None
    form_method = 'POST'
    submit_text = 'Submit'
    field_css = [ 'form-control' ]

    def __init__(self, request, *args, **kwargs):
        '''Constructor'''
        # save the request object
        self.request = request

        # any extra kwargs should be set on this object
        for name in tuple(kwargs.keys()):
            if name not in formsig.parameters:
                setattr(self, name, kwargs.pop(name))

        # create the arguments for the super call, adding `data` and `files` if needed
        # then call the superclass (calling old-fashioned way because self is in the args)
        super_args = formsig.bind(self, *args, **kwargs)
        if request.method == 'POST':
            super_args.arguments['data'] = super_args.arguments.get('data', request.POST)
            super_args.arguments['files'] = super_args.arguments.get('files', request.FILES)
        super_args.apply_defaults()
        forms.Form.__init__(*super_args.args, **super_args.kwargs)

        # call the init() as the last thing in the constructor
        # this gives the subclass a hook without having to override __init__ and call super()
        self.init()


    def init(self):
        '''Hook for subclasses to add fields and any other initialization.'''
        pass


    def as_full(self):
        '''Returns the HTML for this form, including <form>, submit, and csrf tags.'''
        # add the bootstrap css
        css = set(self.field_css)
        for field in self.fields.values():
            current = set(( c.strip() for c in field.widget.attrs.get('class', '').split(' ') if c ))
            field.widget.attrs['class'] = ' '.join(css | current)

        # render the string
        return render_template(self.request, 'formlib', 'form.htm', { 'form': self })


    def __str__(self):
        '''Returns the HTML for this form, including <form>, submit, and csrf tags.'''
        return self.as_full()


    def commit(self, *args, **kwargs):
        '''
        Commits the form after it has been validated.
        '''
        pass


