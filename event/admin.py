from django.contrib import admin
from .models import newUser,EventCategory,Event

# Register your models here.
admin.site.register(newUser)
admin.site.register(Event)
admin.site.register(EventCategory)