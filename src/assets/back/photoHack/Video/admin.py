from django.contrib import admin
from .models import Video


class VideoAdmin(admin.ModelAdmin):
    list_display = []
    search_fields = []

    class Meta:
        model = Video


admin.site.register(Video, VideoAdmin)
