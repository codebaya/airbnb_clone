from django.contrib import admin

from .models import Booking


# Register your models here.

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "check_in", "check_out",
    )
    list_filter = (
        "kind",
    )
