from django.shortcuts import render
from django.http import HttpResponseRedirect
from sip.settings.staging import SUCCESS_SSO_AUTH_REDIRECT as DOMAIN

'''
Custom Handler Views For Django Redirect to Frontend
'''


def custom_unauthorized_view(request, exception=None):
    # HTTP 401 Unauthorized
    return HttpResponseRedirect(DOMAIN + 'not-login/')


def custom_permission_denied_view(request, exception=None):
    # HTTP 403 Forbidden
    return HttpResponseRedirect(DOMAIN + 'not-login/')


def custom_not_found_view(request, exception=None):
    # HTTP 404 Not Found
    return HttpResponseRedirect(DOMAIN)
