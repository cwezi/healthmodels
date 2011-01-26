#!/usr/bin/env python
# encoding=utf-8
# maintainer rgaudin

from django.db import models
from django.utils.translation import ugettext_lazy as _
from rapidsms.models import Contact, ExtensibleModelBase
from rapidsms.contrib.locations.models import Location
import datetime

class PatientBase(models.Model):

    class Meta:
        app_label = 'healthmodels'

    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
        (MALE, _(u"Male")),
        (FEMALE, _(u"Female")))

    ACTIVE = 'A'
    INACTIVE = 'I'
    STATUS_CHOICES = (
        (ACTIVE, _(u"Active")),
        (INACTIVE, _(u"Inactive")))

    health_id = models.ForeignKey('HealthId', unique=True, primary_key=True)
    first_name = models.CharField(_(u"First name"), max_length=100)
    middle_name = models.CharField(_(u"Middle name"), max_length=100, \
                                   help_text=_(u"Middle or second name"), \
                                   blank=True)
    last_name = models.CharField(_(u"Last name"), max_length=100, \
                                 help_text=_(u"Family name or surname"))
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birthdate = models.DateField(blank=True, null=True)
    estimated_birthdate = models.BooleanField(default=False)
    deathdate = models.DateField(blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    health_worker = models.ForeignKey('HealthProvider', blank=True, \
                                      related_name='patients', null=True)
    location = models.ForeignKey(Location, blank=True, null=True)
    health_facility = models.ForeignKey('HealthFacility', blank=True, null=True)
    contact = models.ForeignKey(Contact, blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, \
                              default=ACTIVE)

    @property
    def age(self):
        start_date = self.birthdate if type(self.birthdate) == datetime.date else self.birthdate.date()
        end_date = datetime.date.today()
        if self.deathdate is not None:
            end_date = self.deathdate if type(self.deathdate) == datetime.date else self.deathdate.date()
        return end_date - start_date

    @property
    def is_dead(self):
        return bool(self.deathdate)

    def full_name(self):
        # very weak for now
        return _(u"%(first)s %(last)s") % {'first': self.first_name, \
                                           'last': self.last_name}

    def __unicode__(self):
        return self.full_name()


class Patient(PatientBase):
    __metaclass__ = ExtensibleModelBase

    class Meta:
        app_label = 'healthmodels'
        verbose_name = _("Patient")
        verbose_name_plural = _("Patients")
