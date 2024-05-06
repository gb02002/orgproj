from django.contrib import admin
from django.utils.html import format_html

from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'phone', 'is_org_agent', 'document_link')

    def get_full_name(self, obj):
        return f"{obj.name} {obj.surname}"
    get_full_name.short_description = 'Full Name'

    def document_link(self, obj):
        if obj.document_file:
            return format_html('<a href="{0}" target="_blank">{1}</a>', obj.document_file.url, "Review Document")
        else:
            return "No document uploaded"
    document_link.short_description = 'Document'

admin.site.register(UserProfile, UserProfileAdmin)