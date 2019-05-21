# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models import signals
from django.dispatch import receiver
import datetime
from datetime import timedelta
# Create your models here.
from django.contrib.auth.models import User


low = 26
med = 16
high = 8

class Choice(models.Model):
 choice = models.CharField(max_length=300)

 def __unicode__(self):
  return self.choice

class Connection(models.Model):
 owner = models.ForeignKey(User, null=True, related_name = 'connection')
 first_name = models.CharField(max_length=25, null=True)
 last_name = models.CharField(max_length=25, null=True, blank=True)
 dated_connected = models.DateField(null=True, blank=True)
 email = models.EmailField(null=True)
 company = models.CharField(max_length=64, null=True)
 position = models.CharField(max_length=128, null=True)
 connection_level = models.IntegerField(default=3)
 full_name = models.CharField(max_length=250, null=True, blank=True)

 def __unicode__(self):
  return str(self.first_name) + " " + str(self.last_name)

class Contacted(models.Model):
 connection = models.ForeignKey(Connection, blank = False)
 date_contacted = models.DateField(null=True, blank=True)
 contact_type = models.ForeignKey(Choice, null=True, blank=True)

 def __unicode__(self):
  return str(self.connection.owner) + ": " + str(self.connection) + "-" + str(self.date_contacted)

class ToContact(models.Model):
 connection = models.ForeignKey(Connection, blank = False)
 date = models.DateField(null=True, blank=True)
 completed = models.BooleanField(default=False)

 def __unicode__(self):
  return unicode(self.connection.first_name) + " " + unicode(self.connection.last_name)+ " - " + str(self.connection.owner)
 
 def tocontactcount(self):
  return self.completed
  

class Week(models.Model):
 number = models.IntegerField()
 contacts = models.ManyToManyField(ToContact)
 owner = models.ForeignKey(User, null=True)

 def __unicode__(self):
  return unicode(self.number)

#@receiver(signals.post_save, sender=Connection)
def schedule_contact(sender, instance, **kwargs):
	print instance
	date = datetime.date.today()
	date = date_today + timedelta(weeks = low)
	print date
	q = ToContact(connection = instance, date = date)
	q.save()

def reek_range(date):
 year, week, dow = date.isocalendar()
 if dow == 7:
  start_date = date
 else:
  start_date = date - timedelta(dow)
 end_date = start_date + timedelta(6)
 print week, start_date, end_date
 
class emailcapture(models.Model):
 email = models.EmailField()

 def __unicode__(self):
  return self.email
  
class Profile(models.Model):
 user = models.OneToOneField(User, on_delete=models.CASCADE)
 first_name = models.CharField(max_length=25, null=True)
 last_name = models.CharField(max_length=25, null=True, blank=True)
 education = models.CharField(max_length=256, blank=True)
 industry = models.CharField(max_length=256, blank=True)
 job = models.CharField(max_length=256, null=True, blank=True)
 title = models.CharField(max_length=256, null=True, blank=True)
 goal = models.TextField(max_length=1000, blank=True)
 activity = models.CharField(max_length=256, null=True, blank=True)
 email = models.EmailField()
 referralcode = models.CharField(max_length=256, null=True, blank=True)
 
 
 def __unicode__(self):
  return str(self.user)