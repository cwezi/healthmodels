#!/usr/bin/env python
# encoding=utf-8
# maintainer rgaudin

from django.db import models
from django.utils.translation import ugettext_lazy as _
from rapidsms.models import Contact, ExtensibleModelBase
from Patient import Patient


class PatientEncounterBase(models.Model):

    class Meta:
        app_label = 'healthmodels'

    patient = models.ForeignKey(Patient)


class PatientEncounter(PatientEncounterBase):
    __metaclass__ = ExtensibleModelBase

    class Meta:
        app_label = 'healthmodels'
        verbose_name = _("Patient Encounter")
        verbose_name_plural = _("Patient Encounters")
