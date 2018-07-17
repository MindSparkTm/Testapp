# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django import forms
from .models import SignUp


# Register your models here.

class Registerinfo(admin.ModelAdmin):

    list_display = ['id','created','email','mobilenumber']

admin.site.register(SignUp, Registerinfo)




