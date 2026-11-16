from django.contrib import admin

from .forms import VlogPostForm
from .models import VlogPost


@admin.register(VlogPost)
class VlogPostAdmin(admin.ModelAdmin):
    form = VlogPostForm
    list_display = ["title", "author", "category", "published_date", "updated_at"]
    search_fields = ["title", "description", "tags", "author__username"]
    list_filter = ["category", "published_date", "author"]
    ordering = ["-published_date", "-pk"]
    readonly_fields = ["updated_at"]
    fields = ["title", "video_url", "description", "author", "published_date", "category", "tags", "updated_at"]
    list_select_related = ["author"]


admin.site.site_header = "The Little Vlog administration"
admin.site.site_title = "Vlog admin"
