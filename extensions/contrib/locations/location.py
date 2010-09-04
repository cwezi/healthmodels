from django.db import models

class CodedLocation(models.Model):
    code = models.CharField(max_length=50, blank=True, null=True)
    
    class Meta:
        abstract = True
