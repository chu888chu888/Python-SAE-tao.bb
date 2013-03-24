# vim: ai ts=4 sts=4 et sw=4 ft=python
import os
import sys
root = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(root, 'site-packages'))

import sae
from bottle import default_app

import taobb

application = sae.create_wsgi_app(default_app())
