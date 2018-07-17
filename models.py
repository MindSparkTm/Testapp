# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.db import models
from cloudinary.models import CloudinaryField
from django.utils import timezone



from cloudinary.models import CloudinaryField

class SignUp(models.Model):
  id = models.AutoField(primary_key=True)
  created = models.DateTimeField(auto_now_add=True, editable=False)
  email = models.CharField(max_length=200, null=True, blank=True)
  mobilenumber = models.CharField(max_length=200, null=True, blank=True)
  password = models.CharField(max_length=200, null=True, blank=True)



