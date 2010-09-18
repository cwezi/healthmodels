#!/usr/bin/env python
# encoding=utf-8
# maintainer rgaudin

from django.db import models
from django.utils.translation import ugettext_lazy as _
from rapidsms.models import Contact, ExtensibleModelBase
from HealthFacility import HealthFacility


class FacilityReportBase(models.Model):

    class Meta:
        app_label = 'healthmodels'

    facility = models.ForeignKey(HealthFacility)


class FacilityReport(FacilityReportBase):
    __metaclass__ = ExtensibleModelBase

    class Meta:
        app_label = 'healthmodels'
        verbose_name = _("Facility Report")
        verbose_name_plural = _("Facility Reports")
