"""
WSGI config for retail_sale project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'retail_sale.settings')

project_folder = os.path.expanduser('~/Code/sales_project/retail_sale')

application = get_wsgi_application()
