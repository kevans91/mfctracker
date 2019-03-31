#  Copyright (c) 2016-2019 Oleksandr Tymoshenko <gonzo@bluezbox.com>
#  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions
#  are met:
#  1. Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#  2. Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#
#  THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
#  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
#  ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
#  FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
#  OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
#  HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
#  LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
#  OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
#  SUCH DAMAGE.
"""
Django settings for mfctracker project.

Generated by 'django-admin startproject' using Django 1.10.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os.path as op
import os
import environ

from django.utils.crypto import get_random_string

GLOBAL_ENV = '/usr/local/etc/mfctracker.env'
LOCAL_ENV = 'env'

root = environ.Path(__file__) - 3 # three folder back (/a/b/c/ - 3 = /)
env = environ.Env()

SECRET_KEY = env('SECRET_KEY', default=get_random_string(length=40))

if os.path.exists(GLOBAL_ENV):
       environ.Env.read_env(GLOBAL_ENV)
if os.path.exists(root(LOCAL_ENV)):
       environ.Env.read_env(root(LOCAL_ENV))

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = root()

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.auth',
    'bootstrap3',
    'mfctracker',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mfctracker.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'mfctracker.context_processors.branches',
                'mfctracker.context_processors.ldap',
            ],
        },
    },
]

WSGI_APPLICATION = 'mfctracker.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    op.join(BASE_DIR, "static"),
]

LOGIN_REDIRECT_URL = '/'

SVN_EMAIL_DOMAIN = 'freebsd.org'
SVN_BASE_URL = 'http://svn.freebsd.org/base'
VIEWVC_REVISION_URL = 'http://svnweb.freebsd.org/changeset/base/{revision}'

TEST_RUNNER = 'django_pytest.test_runner.TestRunner'

EMAIL_CONFIG = env.email_url('EMAIL_URL', default='smtp://localhost:25')

vars().update(EMAIL_CONFIG)
DEFAULT_FROM_EMAIL = env.str('DEFAULT_FROM_EMAIL', default='mfctracker@localhost')

DATABASES = {
    'default': env.db(default='pgsql://mfctracker@localhost/mfctracker'),
}

AUTH_LDAP_ENABLED = env.bool('AUTH_LDAP_ENABLED', default=False)
if AUTH_LDAP_ENABLED:
    import ldap
    from django_auth_ldap.config import LDAPSearch
    AUTHENTICATION_BACKENDS = (
        'django_auth_ldap.backend.LDAPBackend',
        'django.contrib.auth.backends.ModelBackend',
    )

    ldap.set_option(ldap.OPT_REFERRALS, 0)
    AUTH_LDAP_SERVER_URI = env.str('AUTH_LDAP_SERVER_URI') # no default, required
    AUTH_LDAP_BIND_DN = env.str('AUTH_LDAP_BIND_DN', default='')
    AUTH_LDAP_BIND_PASSWORD = env.str('AUTH_LDAP_BIND_PASSWORD', default='')
    ldap_search_base = env.str('AUTH_LDAP_USER_SEARCH_BASE') # no default, required
    ldap_search_filter = env.str('AUTH_LDAP_USER_SEARCH_FILTER', default='(uid=%(user)s)')
    AUTH_LDAP_USER_SEARCH = LDAPSearch(ldap_search_base,
        ldap.SCOPE_SUBTREE, ldap_search_filter)
