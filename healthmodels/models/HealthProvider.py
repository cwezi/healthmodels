#!/usr/bin/env python
# encoding=utf-8
# maintainer rgaudin

from django.db import models
from django.utils.translation import ugettext_lazy as _
from rapidsms.models import Contact, ExtensibleModelBase
from simple_locations.models import Area

class HealthProviderBase(Contact):

    class Meta:
        app_label = 'healthmodels'

    facility = models.ForeignKey('HealthFacility', null=True)
    location = models.ForeignKey(Area, null=True)


class HealthProvider(HealthProviderBase):
    __metaclass__ = ExtensibleModelBase

    class Meta:
        app_label = 'healthmodels'
        verbose_name = _("Health Provider")
        verbose_name_plural = _("Health Providers")
