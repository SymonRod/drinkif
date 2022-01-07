from django.db import models
from django.contrib.auth.models import User

class phrases(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    phrase_text = models.CharField(max_length=300)