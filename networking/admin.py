# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Contacted, Connection, Choice, ToContact, Week, emailcapture
# Register your models here.
#class ConnectionAdmin(admin.ModelAdmin):
#    pass
#admin.site.register(Connection, ConnectionAdmin)
#
#class ContactAdmin(admin.ModelAdmin):
#    pass
#admin.site.register(Contact, ContactAdmin)
#
#class ChoiceAdmin(admin.ModelAdmin):
#    pass
#admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Contacted)
admin.site.register(Connection)
admin.site.register(Choice)
admin.site.register(ToContact)
admin.site.register(Week)
admin.site.register(emailcapture)