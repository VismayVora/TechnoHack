from django.contrib import admin
from .models import MyUser, Guardian, Location, AuditForm
# Register your models here.
admin.site.register(MyUser)
admin.site.register(Guardian)
admin.site.register(Location)
admin.site.register(AuditForm)