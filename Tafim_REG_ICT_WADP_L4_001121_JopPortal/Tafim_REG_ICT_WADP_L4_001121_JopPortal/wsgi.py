"""
WSGI config for Tafim_REG_ICT_WADP_L4_001121_JopPortal project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tafim_REG_ICT_WADP_L4_001121_JopPortal.settings')

application = get_wsgi_application()
