from django.db import models
from django.contrib.auth.models import User

class Validation(models.Model):
    STATUS_CHOICES = [
        ("DRAFT","DRAFT"),
        ("PROCESSED", "PROCESSED"),
        ("ERROR", "ERROR"),
    ]

    title = models.CharField(max_length=200) 
    status= models.CharField(max_length=20, choices=STATUS_CHOICES, default="DRAFT")

    extracted_key = models.CharField(max_length=50, blank=True, null=True)
    extracted_value = models.CharField(max_length=200, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="validations")

    def __str__(self):
        return f"{self.id} - {self.title}"
    