from django.contrib import admin

from compare.models import Person, Compare, Expert

admin.site.register(Person)
admin.site.register(Expert)
admin.site.register(Compare)
