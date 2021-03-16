from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

from .models import Poll, Question

admin.site.register(Question)


@admin.register(Poll)
class PollModelAdmin(ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["start_date"]
        else:
            return []
