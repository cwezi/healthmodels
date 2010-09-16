#!/usr/bin/env python
# encoding=utf-8
# maintainer rgaudin

from django.db import models
from django.utils.translation import ugettext_lazy as _
from treebeard.mp_tree import MP_Node
from rapidsms.contrib.locations.models import Location, LocationType
from rapidsms.models import Contact, ExtensibleModelBase


class HealthFacilityBase(MP_Node):


    class Meta:
        app_label = 'healthmodels'

    type = models.ForeignKey(LocationType)
    # Catchment area should be a location that makes sense independently, i.e.
    # a city, town, village, parish, region, district, etc.
    catchment_area = models.ForeignKey(Location, null=True, \
                                       related_name='main_health_facilities')
    # location is the physical location of the health facility itself.
    # This location should only represent the facility's location, and
    # shouldn't be overloaded to also represent the location of a town
    # or village.  Depending on pending changes to the locations model,
    # this could eventually be a ForeignKey to the Point class instead.
    location = models.ForeignKey(Location, null=True, \
                                 related_name='all_health_facilities')
    code = models.CharField(max_length=50, blank=True, null=True)


class HealthFacility(HealthFacilityBase):
    __metaclass__ = ExtensibleModelBase


    class Meta:
        app_label = 'healthmodels'
