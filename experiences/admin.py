from django.contrib import admin

from .models import Experience, Perk


# Register your models here.
@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = (
        "name", "host", "price", "address",
    )
    list_filter = (
        "name", "price", "host", "address", "category"
    )


@admin.register(Perk)
class PerkAdmin(admin.ModelAdmin):
    list_display = (
        "name", "details", "explanation",
    )
