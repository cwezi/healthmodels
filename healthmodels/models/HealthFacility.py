#!/usr/bin/env python
# encoding=utf-8
# maintainer rgaudin

from random import choice

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from rapidsms.models import ExtensibleModelBase
from simple_locations.models import Area, Point


class HealthFacilityTypeBase(models.Model):

    class Meta:
        app_label = 'healthmodels'

    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=30, unique=True)

    def __unicode__(self):
        return self.name


class HealthFacilityType(HealthFacilityTypeBase):
    __metaclass__ = ExtensibleModelBase

    class Meta:
        app_label = 'healthmodels'
        verbose_name = _("Health Facility Type")
        verbose_name_plural = _("Health Facility Types")


class HealthFacilityBase(models.Model):

    class Meta:
        app_label = 'healthmodels'

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, blank=True, null=False)
    type = models.ForeignKey(HealthFacilityType, blank=True, null=True)
    # Catchment areas should be locations that makes sense independently, i.e.
    # a city, town, village, parish, region, district, etc.
    catchment_areas = models.ManyToManyField(Area, null=True, blank=True)
    # location is the physical location of the health facility itself.
    # This location should only represent the facility's location, and
    # shouldn't be overloaded to also represent the location of a town
    # or village.  Depending on pending changes to the locations model,
    # this could eventually be a ForeignKey to the Point class instead.
    location = models.ForeignKey(Point, null=True, blank=True)
    # report_to generic relation.
    report_to_type = models.ForeignKey(ContentType, null=True, blank=True)
    report_to_id = models.PositiveIntegerField(null=True, blank=True)
    report_to = generic.GenericForeignKey('report_to_type', 'report_to_id')

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        ''' generates a code if none provided '''
        if not self.code:
            # generation is dumb now and not conflict-safe
            # probably suffiscient to handle human entry through django-admin
            chars = '1234567890_QWERTYUOPASDFGHJKLZXCVBNM'
            self.code = u"gen" + u"".join([choice(chars) \
                                          for i in range(10)]).lower()
        super(HealthFacilityBase, self).save(*args, **kwargs)


class HealthFacility(HealthFacilityBase):
    __metaclass__ = ExtensibleModelBase

    class Meta:
        app_label = 'healthmodels'
        verbose_name = _("Health Facility")
        verbose_name_plural = _("Health Facilities")
    def is_root(self):
        if self.report_to==None:
            return True
        else:
            return False
    def get_children(self):

            children=HealthFacility.objects.filter(report_to_id=self.pk)
            if len(children)>0:
                return children
            else:
                return False
    def is_child_node(self):
        children=HealthFacility.objects.filter(report_to_id=self.pk)
        if len(children>0):
            return False
        else:
            return True
    
            


       
    
