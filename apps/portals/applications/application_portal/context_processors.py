#!/usr/bin/python
# -*- coding: utf-8 -*-

def site_url(request):
    """
        This is the context processor for templates to provide the base url of the site
    """
    from django.conf import settings
    return {'site_url': settings.SITE_URL}
