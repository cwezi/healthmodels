from django.conf import settings
from django.db import models
from rapidsms.contrib.locations.models import Location, LocationType
from rapidsms.models import Contact, ExtensibleModelBase
from treebeard.mp_tree import MP_Node

class HealthIdBase(models.Model):
    """
    Health Id is a unique identifier for a patient, but can also correspond
    to a physical ID in places where these exist (hence the separate class).
    This class is designed to err on the side of *too much* information, as 
    for simpler MIS systems this class may be completely unused.
    
    An important field to note is migration_id.  This field is here optimistically.  Ideally, one day, all mHealth
    projects will do a monolithic migration to a universal MIS with
    universal health ids.  This would serve as a placeholder to make
    the migration easy at an API level: each internal app could use
    its own health_id internally within it's existing models,
    while exposing the public migration_id to the outside world. 
    """
    class Meta:
        verbose_name = u"Health ID"
        verbose_name_plural = u"Health IDs"

    STATUS_GENERATED = 'G'
    STATUS_PRINTED = 'P'
    STATUS_ISSUED = 'I'
    STATUS_REVOKED = 'R'

    STATUS_CHOICES = (
        (STATUS_GENERATED, u"Generated"),
        (STATUS_PRINTED, u"Printed"),
        (STATUS_ISSUED, u"Issued"),
        (STATUS_REVOKED, u"Revoked"))

    health_id = models.CharField(u"Health ID", max_length=10, unique=True)
    generated_on = models.DateTimeField(u"Generated on", auto_now_add=True)
    printed_on = models.DateTimeField(u"Printed on", blank=True, null=True)
    issued_on = models.DateTimeField(u"Issued on", blank=True, null=True)
    revoked_on = models.DateTimeField(u"Revoked on", blank=True, null=True)
    issued_to = models.ForeignKey('Patient', verbose_name=u"Issued to", \
                                  blank=True, null=True)
    status = models.CharField(u"Status", choices=STATUS_CHOICES, \
                              max_length=1, default=STATUS_GENERATED)
    
    migration_id = models.BigIntegerField(unique=True,null=True)

    def __unicode__(self):
        return u"%s" % self.health_id

class HealthFacilityBase(MP_Node):
    type = models.ForeignKey(LocationType)
    # Catchment area should be a location that makes sense independently, i.e.
    # a city, town, village, parish, region, district, etc.
    catchment_area = models.ForeignKey(Location, null=True, related_name='main_health_facilities')
    # location is the physical location of the health facility itself.
    # This location should only represent the facility's location, and
    # shouldn't be overloaded to also represent the location of a town
    # or village.  Depending on pending changes to the locations model,
    # this could eventually be a ForeignKey to the Point class instead.
    location = models.ForeignKey(Location, null=True, related_name='all_health_facilities')
    code = models.CharField(max_length=50, blank=True, null=True)

class HealthProviderBase(Contact):
    facility = models.ForeignKey('HealthFacility', null=True)
    location = models.ForeignKey(Location, null=True)
    
class PatientBase(models.Model):
    health_id = models.ForeignKey('HealthId', unique=True, primary_key=True)
    name = models.CharField(max_length=128)
    gender = models.CharField(max_length=1, choices=(('M', 'Male'),('F', 'Female')), null=True)
    birthdate = models.DateField(null=True)
    estimated_birthdate = models.BooleanField(default=False)
    deathdate = models.DateField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    health_worker = models.ForeignKey('HealthProvider', null=True, related_name='patients')
    location = models.ForeignKey(Location, null=True)
    health_facility = models.ForeignKey('HealthFacility', null=True)
    contact = models.ForeignKey(Contact, null=True)
    status  = models.CharField(max_length=1, choices=(('A', 'Active'),('I', 'Inactive')))

    @property
    def first_name(self):
        names = self.name.split(' ')
        if settings.SURNAME_FIRST and len(names) > 1:
            return names[1]
        else:
            return names[0]
    
    @property
    def last_name(self):
        names = self.name.split(' ')
        if not settings.SURNAME_FIRST and len(names) > 1:
            return names[len(names) - 1]
        else:
            return names[0]
    
    @property
    def age(self):
        end_date = self.deathdate if self.deathdate else self.datetime.now()
        return end_date - self.birthdate
    
    @property
    def is_dead(self):
        return bool(self.deathdate)

class Patient(PatientBase):
    __metaclass__ = ExtensibleModelBase
    
class HealthFacility(HealthFacilityBase):
    __metaclass__ = ExtensibleModelBase
    
class PatientEncounterBase(models.Model):
    patient = models.ForeignKey(Patient)

class FacilityReportBase(models.Model):
    facility = models.ForeignKey(HealthFacility)

class HealthProvider(HealthProviderBase):
    __metaclass__ = ExtensibleModelBase
    
class HealthId(HealthIdBase):
    __metaclass__ = ExtensibleModelBase

class PatientEncounter(PatientEncounterBase):
    __metaclass__ = ExtensibleModelBase

class FacilityReport(FacilityReportBase):
    __metaclass__ = ExtensibleModelBase

