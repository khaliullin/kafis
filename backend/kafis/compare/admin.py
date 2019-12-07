from django.contrib import admin

from compare.models import Person, Compare, Expert, Report


class PersonAdmin(admin.ModelAdmin):
    search_fields = ['name', 'id', 'vk_id']


admin.site.register(Person, PersonAdmin)
admin.site.register(Expert)
admin.site.register(Compare)
admin.site.register(Report)
