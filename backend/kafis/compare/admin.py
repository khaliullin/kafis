from django.contrib import admin

from compare.models import Person, Compare, Expert, Report

admin.site.register(Person)
admin.site.register(Expert)
admin.site.register(Compare)
admin.site.register(Report)
