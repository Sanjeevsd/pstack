from django.contrib import admin
from .models import usersprofile, projects,ContactForm

# Register your models here.

admin.site.register(usersprofile)
admin.site.register(projects)
admin.site.register(ContactForm)
