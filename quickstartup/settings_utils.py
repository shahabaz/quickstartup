# coding: utf-8
#
# Extract heavy logic from settings.py, manage.py and wsgi.py
#


import logging

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string


class CustomAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        messages = []
        data = kwargs.get('extra', {})
        for key, value in sorted(data.items()):
            if "pass" in key:
                value = '*' * 6

            messages.append('{}={!r}'.format(key, value))
        return '{} {}'.format(msg, ', '.join(messages)), kwargs


def get_logger(name):
    return CustomAdapter(logging.getLogger(name), {})


def get_loggers(level, loggers):
    logging.addLevelName('DISABLED', logging.CRITICAL + 10)

    log_config = {
        'handlers': ['console'],
        'level': level,
    }

    if level == 'DISABLED':
        loggers = {'': {'handlers': ['null'], 'level': 'DEBUG', 'propagate': False}}
    else:
        loggers = {logger.strip(): log_config for logger in loggers}

    return loggers


def get_project_package(project_dir):
    if (project_dir / "project_name").exists():
        project_name = "project_name"
    else:
        settings_files = list(project_dir.glob("*/settings.py"))
        if len(settings_files) != 1:
            raise ImproperlyConfigured("settings.py not found or found more than one")
        project_name = settings_files[0].parent.name

    return project_name


def get_static_root(base_dir):
    try:
        # noinspection PyUnresolvedReferences
        from dj_static import Cling
    except ImportError:
        return str(base_dir / "static")

    return "staticfiles"


def get_media_root(base_dir):
    try:
        # noinspection PyUnresolvedReferences
        from dj_static import MediaCling
    except ImportError:
        return str(base_dir / "media")

    return "media"


DEFAULT_SETTINGS = {
    'LOGIN_REDIRECT_URL': 'app:index',
    'QS_PROJECT_NAME': 'Django Quickstartup',
    'QS_PROJECT_CONTACT': 'contact@quickstartup.us',
    'QS_PROJECT_DOMAIN': 'quickstartup.us',
    'QS_PROJECT_URL': 'https://quickstartup.us',
    'QS_PROFILE_FORM': 'quickstartup.qs_accounts.forms.ProfileForm',
    'QS_PASSWORD_FORM': 'quickstartup.qs_accounts.forms.SetPasswordForm',
    'QS_PASSWORD_CHANGE_FORM': 'django.contrib.auth.forms.PasswordChangeForm',
    'QS_SIGNUP_OPEN': True,
    'QS_SIGNUP_FORM': 'quickstartup.qs_accounts.forms.SignupForm',
    'QS_SIGNUP_AUTO_LOGIN': False,
    'QS_SIGNUP_TOKEN_EXPIRATION_DAYS': 7,
    'QS_CONTACT_FORM': 'quickstartup.qs_contacts.forms.ContactForm',
}


def get_settings(name):
    return getattr(settings, name.upper(), DEFAULT_SETTINGS.get(name))


def get_object_from_settings(name):
    return import_string(get_settings(name))