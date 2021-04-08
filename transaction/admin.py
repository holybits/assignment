from django.contrib import admin
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
from transaction.models import *


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "amount", "type", "parent_id", "created", "updated")

    list_display_links = ("id",)
    search_fields = ("id", "amount","type" )
    ordering = ("-id",)
    list_filter = ("type",)
    actions_on_bottom = False
    actions_on_top = True
