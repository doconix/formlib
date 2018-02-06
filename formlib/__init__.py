# All apps that are DMP-enabled must have this setting in their app-level __init__.py
DJANGO_MAKO_PLUS = True

# include Formless in the package namespace
from .form import Formless