"""Custom Admin Panel"""
from django.contrib import admin
from municipio_invest.api.core.models import (
    Municipality,
    Contract,
    District,
    NUTSIII
)

@admin.register(Municipality)
class MunicipalityAdminPage(admin.ModelAdmin):
    list_display = ["name", "district", "nuts_III"]
    search_fields = ["name", "district__name", "nuts_III__name"]
    autocomplete_fields = ["district", "nuts_III"]

@admin.register(Contract)
class ContractAdminPage(admin.ModelAdmin):
    list_display = [
        "contracting_party__name",
        "contracted",
        "contract_price",
        "signing_date"
    ]
    search_fields = [
        "contracting_party__name",
        "contracted",
        "contract_type",
        "description"
        "contract_price",
        "signing_date"
    ]
    autocomplete_fields = ["contracting_party",]

@admin.register(NUTSIII)
class NUTSIIIAdminPage(admin.ModelAdmin):
    list_display = ["name",]
    search_fields = ["name",]

@admin.register(District)
class DistrictAdminPage(admin.ModelAdmin):
    list_display = ["name",]
    search_fields = ["name",]
