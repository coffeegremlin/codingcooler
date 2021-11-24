from django.contrib import admin

from .models import Project, Resource, Step, Wireframe
# Register your models here.
admin.site.register(Project)
admin.site.register(Resource)
admin.site.register(Step)
admin.site.register(Wireframe)