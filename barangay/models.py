from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.utils.crypto import get_random_string
import random
import string

ROLES = (
    ('1', 'officials'),
    ('2', 'visitors')
)


stat = (
    (1, 'Lock'),
    (2, 'Unclock')
)



class calibrations(models.Model):
    sensor_hieght  = models.FloatField(verbose_name="Sensors Height")
    setting_height = models.FloatField(verbose_name="Setting Height")
    low_threshold = models.FloatField(verbose_name="Low Threshold")
    mediun_threshold = models.FloatField(verbose_name="Medium Threshold")
    heigh_threshold = models.FloatField(verbose_name="High Threshold")


class controls(models.Model):
    '''Model definition for controls.'''
    control = models.IntegerField(choices=stat)
    site = models.CharField(max_length=50)
    class Meta:

        verbose_name = 'controls'
        verbose_name_plural = 'controls'


class user_roles(models.Model):
    role = models.CharField(max_length=50)
    def __str__(self):
        return self.role

class User(AbstractUser):
    userrole = models.ForeignKey("user_roles", verbose_name=("user roles"), on_delete=models.SET_NULL, null=True)
    fname = models.CharField(verbose_name="First Name",max_length=100, null=True)
    lname = models.CharField(verbose_name="Last Name",max_length=100, null=True)
    middle = models.CharField(verbose_name="Middle Name", max_length=50)
    Address = models.CharField(max_length=200, null=True)
    Contact = models.IntegerField(null=True)
    email = models.EmailField(unique=True, null=True)
    roles = models.CharField(choices=ROLES, default='2', max_length=50)  
    avatar = models.ImageField(upload_to="Profiles", null=True, default="Profiles/avatar.png")
    code = models.IntegerField(blank=True, null=True)  # Allow blank and null values
    status = models.CharField(default="notverified", max_length=50)
    lock = models.CharField(max_length=50, default='none')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
