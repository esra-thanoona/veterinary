from django.contrib import admin

from veterinaryapp import models

# Register your models here.
admin.site.register(models.Login)
admin.site.register(models.Doctor)
admin.site.register(models.Patients)