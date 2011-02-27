#!/usr/bin/env python
# encoding=utf-8
# maintainer rgaudin

from django.contrib import admin

from models import *

admin.site.register(HealthId)
admin.site.register(HealthProvider)
admin.site.register(Patient)
admin.site.register(PatientEncounter)
admin.site.register(FacilityReport)


class HealthFacilityTypeAdmin(admin.ModelAdmin):
    pass


class HealthFacilityAdmin(admin.ModelAdmin):
    pass

admin.site.register(HealthFacility, HealthFacilityAdmin)
admin.site.register(HealthFacilityType, HealthFacilityTypeAdmin)
