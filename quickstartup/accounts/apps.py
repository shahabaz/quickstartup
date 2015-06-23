# coding: utf-8


from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AccountConfig(AppConfig):
    name = 'quickstartup.accounts'
    verbose_name = _("Accounts")
