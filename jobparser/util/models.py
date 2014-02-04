from django.db import models

# Create your models here.
class Job(models.Model):
    company_name = models.CharField(max_length=300, blank=True, null=True)
    company_id = models.CharField(max_length=300, blank=True, null=True)
    source = models.CharField(max_length=300, blank=True, null=True)
    title = models.CharField(max_length=300, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    qualification = models.TextField(blank=True, null=True)
    all_text = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=600, blank=True, null=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    posting_date = models.DateTimeField(null=True, blank=True)
    source_joburl = models.CharField(max_length=900, blank=True, null=True)
    company_joburl = models.CharField(max_length=900, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now=True)