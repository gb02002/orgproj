from django.contrib import admin
from django.contrib.gis.forms import PointField, OSMWidget
from django.contrib.gis.admin import GISModelAdmin
from django.db.models import OuterRef, Subquery
from django.utils.html import format_html
from .models import Organisation, Locations, FilterforLocation, LocationMedia


# Register your models here.

@admin.register(LocationMedia)
class MediaAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width: 200px; max-height: 200px;" />'.format(obj.image.url))

    image_tag.short_description = 'Image'

    list_display = ['location', 'description', 'image_tag']

    readonly_fields = ['image_tag']


@admin.register(Locations)
class LocationsAdmin(GISModelAdmin):
    formfield_overrides = {
        PointField: {"widget": OSMWidget},
    }
    list_display = ['location_name', 'address', 'open_hours', 'point']


class LocationInline(admin.TabularInline):
    model = Locations
    extra = 0


@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ['organisation', 'title', 'desc', 'mail', 'phone', 'web', ]
    search_fields = ['title', 'desc']
    inlines = [LocationInline]
    ordering = ['locations', ]

    # def get_queryset(self, request):
    #     subquery = Organisation.objects.filter(organisation=OuterRef('organisation')).order_by('organisation')

    #     queryset = Organisation.objects.filter(
    #         id=Subquery(subquery.values('organisation')[:1])
    #     )


admin.site.register(FilterforLocation)
