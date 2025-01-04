#booleanSearch/models.py

from django.db import models

class Candidate(models.Model):
    """
    A model representing a candidate with a profile.
    """
    name = models.CharField(max_length=255, help_text="Full name of the candidate")
    profile = models.TextField(help_text="Description or profile information of the candidate")
    email = models.EmailField(unique=True, help_text="Email address of the candidate")
    phone = models.CharField(max_length=15, blank=True, null=True, help_text="Phone number of the candidate")
    skills = models.CharField(max_length=255, blank=True, help_text="Comma-separated list of skills")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
