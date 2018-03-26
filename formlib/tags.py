from .form import Formless
from mako.runtime import supports_caller, capture



@supports_caller
def render(context, form='form'):
    '''
    Renders the form by the given name within the context.

    The primary advantage to using this tag (instead of simply ${ form }) is
    you can place additional html content within the tag, which prints
    at the bottom of the form.

    The `form` parameter can be a form object or form name (str) within the context.

    # Use the context variable "form".
        <%namespace name="fl" module="formlib.tags"/>
        <%fl:render/>

    # Form by name (context key):
        <%namespace name="fl" module="formlib.tags"/>
        <%fl:render form='form_key'/>

    # Direct reference to form object:
        <%namespace name="fl" module="formlib.tags"/>
        <%fl:render form='${ form_obj }'/>
    '''
    formobj = form
    if isinstance(form, str):
        formobj = context.get(form)
        if formobj is None:
            raise ValueError('Context key `{}` not found'.format(form))
    if not isinstance(formobj, Formless):
        raise ValueError('Object {} is not a Formless subclass'.format(formobj))

    extra = capture(context, context['caller'].body)
    return formobj.as_full(extra=extra)
