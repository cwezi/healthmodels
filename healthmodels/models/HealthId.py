#!/usr/bin/env python
# encoding=utf-8
# maintainer rgaudin

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from rapidsms.models import Contact, ExtensibleModelBase


class HealthIdBase(models.Model):
    """
    Health Id is a unique identifier for a patient, but can also correspond
    to a physical ID in places where these exist (hence the separate class).
    This class is designed to err on the side of *too much* information, as
    for simpler MIS systems this class may be completely unused.

    An important field to note is migration_id.
    This field is here optimistically.  Ideally, one day, all mHealth
    projects will do a monolithic migration to a universal MIS with
    universal health ids.  This would serve as a placeholder to make
    the migration easy at an API level: each internal app could use
    its own health_id internally within it's existing models,
    while exposing the public migration_id to the outside world.
    """

    class Meta:
        app_label = 'healthmodels'
        verbose_name = _(u"Health ID")
        verbose_name_plural = _(u"Health IDs")

    GENERATED = 'G'
    PRINTED = 'P'
    ISSUED = 'I'
    REVOKED = 'R'

    STATUS_CHOICES = (
        (GENERATED, u"Generated"),
        (PRINTED, u"Printed"),
        (ISSUED, u"Issued"),
        (REVOKED, u"Revoked"))

    health_id = models.CharField(_(u"Health ID"), max_length=10, unique=True)
    generated_on = models.DateTimeField(_(u"Generated on"), auto_now_add=True)
    printed_on = models.DateTimeField(_(u"Printed on"), blank=True, null=True)
    issued_on = models.DateTimeField(_(u"Issued on"), blank=True, null=True)
    revoked_on = models.DateTimeField(_(u"Revoked on"), blank=True, null=True)
    issued_to = models.ForeignKey('Patient', verbose_name=_(u"Issued to"), \
                                  blank=True, null=True)
    status = models.CharField(_(u"Status"), choices=STATUS_CHOICES, \
                              max_length=1, default=GENERATED)

    #migration_id = models.BigIntegerField(unique=True, null=True)

    def __unicode__(self):
        return ugettext(u"%s") % self.health_id


class HealthId(HealthIdBase):
    __metaclass__ = ExtensibleModelBase

    class Meta:
        app_label = 'healthmodels'
        verbose_name = _("Health ID")
        verbose_name_plural = _("Health IDs")
