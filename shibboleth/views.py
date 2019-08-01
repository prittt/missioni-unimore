from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.http import HttpRequest, HttpResponse
from django.shortcuts import HttpResponseRedirect, resolve_url
from django.conf import settings
from codicefiscale import codicefiscale
from comuni_italiani.models import *

import datetime
import json

def get_success_url(request):
    url = request.POST.get('next', request.GET.get('next', ''))
    return url or resolve_url(settings.LOGIN_REDIRECT_URL)


def shibboleth_login(request, flag):
    meta = request.META

    user, created = User.objects.get_or_create(username=meta["eppn"])
    if created:
        user.set_unusable_password()

    if user.email == '' and "mail" in meta:
        user.email = meta["mail"]
    if user.first_name == '' and "givenName" in meta:
        user.first_name = str(meta["givenName"]).capitalize()
    if user.last_name == '' and "sn" in meta:
        user.last_name = str(meta["sn"]).capitalize()

    user.save()

    if flag:
        cf = ''
        if 'unimorecodicefiscale' in meta:
            cf = codicefiscale.decode(meta['unimorecodicefiscale'])
            if user.profile.data_nascita is None and cf != '':
                user.profile.data_nascita = cf['birthdate']
            if user.profile.luogo_nascita is None and cf != '':
                luogo_nascita = cf['birthplace']['name'].lower()
                user.profile.luogo_nascita = Comune.objects.filter(name=luogo_nascita)[0]
            if user.profile.sesso is None and cf != '':
                user.profile.sesso = cf['sex']
        if user.profile.qualifica is None:
            pass
        user.save()

    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)

    request.GET.urlencode()
    return HttpResponseRedirect(get_success_url(request))


def shibboleth_test(request: HttpRequest):
    meta = request.META

    s = '<pre>\n'
    for k, v in meta.items():
        s += k + ': ' + str(v) + '\n'
    s += '</pre>\n'

    return HttpResponse(s)
