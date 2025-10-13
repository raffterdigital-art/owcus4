from django.contrib import admin
from .models import School, StudentProfile, SchoolPost, StudentChat

admin.site.register(School)
admin.site.register(StudentProfile)
admin.site.register(SchoolPost)
admin.site.register(StudentChat)