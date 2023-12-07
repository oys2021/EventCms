from django.contrib import admin
from .models import newUser,EventCategory,Event,RegisteredUser

# Register your models here.
admin.site.register(newUser)
admin.site.register(Event)
admin.site.register(EventCategory)
admin.site.register(RegisteredUser)