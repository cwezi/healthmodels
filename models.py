from django.db import models

from treebeard.mp_tree import MP_Node

from rapidsms.models import ExtensibleModelBase
from rapidsms.models import Contact
from rapidsms.contrib.locations.models import Location

class HealthId(models.Model):
    
    pass

class HealthFacilityType(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, primary_key=True)

class HealthFacilityBase(MP_Node):
    type = models.ForeignKey(HealthFacilityType)
    # Catchment area should be a location that makes sense independently, i.e.
    # a city, town, village, parish, region, district, etc.
    catchment_area = models.ForeignKey(Location, null=True)
    # location is the physical location of the health facility itself.
    # This location should only represent the facility's location, and
    # shouldn't be overloaded to also represent the location of a town
    # or village.  Depending on pending changes to the locations model,
    # this could eventually be a ForeignKey to the Point class instead.
    location = models.ForeignKey(Location, null=True)
    code = models.CharField(max_length=50, blank=True, null=True)

class HealthProviderBase(Contact):
    facility = models.ForeignKey('HealthFacility', null=True)
    location = models.ForeignKey(Location, null=True)
    
class PatientBase(models.Model):
    """
    I write awesome documentation
    """
    health_id = models.ForeignKey(HealthId, unique=True, primary_key=True)
    name = models.CharField(max_length=128)
    gender = models.CharField(max_length=1, choices=(('M', 'Male'),('F', 'Female')), null=True)
    birthdate = models.DateField(null=True)
    estimated_birthdate = models.BooleanField(default=False)
    deathdate = models.DateField(null=True)
    created = models.DateTimeField(auto_add_now=True)
    updated = models.DateTimeField(auto_now=True)
    health_worker = models.ForeignKey(HealthProvider, null=True)
    location = models.ForeignKey(Location, null=True)
    health_facility = models.ForeignKey(HealthFacility, null=True)
    contact = models.ForeignKey(Contact, null=True)
    status  = models.CharField(max_length=1, choices=(('A', 'Active'),('I', 'Inactive')))

    @property
    def first_name(self):
        pass
    
    @property
    def last_name(self):
        pass
    
    @property
    def age(self):
        pass
    
    @property
    def is_dead(self):
        return bool(self.deathdate)

    class Meta:
        abstract = True

class Patient(PatientBase):
    __metaclass__ = ExtensibleModelBase
    
class HealthFacility(HealthFacilityBase):
    __metaclass__ = ExtensibleModelBase
    
class HealthProvider(HealthProviderBase):
    __metaclass__ = ExtensibleModelBase    