# formlib
Making Django forms easier, one DRY code line at a time.

This is a very simple superclass for Django forms.  It serves as boilerplate code.

It is released under the Apache open source license as part of the IS 413 course at Brigham Young University.  Everything is standard Django except templates/form.htm, which uses the [Django Mako Plus](https://github.com/doconix/django-mako-plus) templating engine.  This can easily be fixed to work with Django's normal templating engine.

# Installation

Download the code, and place the `formlib` directory in your project root.  Then add `formlib` to your `INSTALLED_APPS`.

See [/formlib/form.py](https://github.com/doconix/formlib/blob/master/formlib/form.py) for example code.