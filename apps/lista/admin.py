from django.contrib import admin
from lista.models import Teacher


class TeacherAdmin(admin.ModelAdmin):
    fields = ('degree', ('name', 'surname'), 'faculty')
    list_display_links = ['surname', 'name']
    list_display = ['degree', 'name', 'surname', 'faculty']
    ordering = ['surname']
    search_fields = ['surname']
    list_filter = ['faculty']
    list_per_page = 250


admin.site.register(Teacher, TeacherAdmin)


