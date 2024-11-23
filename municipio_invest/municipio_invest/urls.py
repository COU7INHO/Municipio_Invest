from django.contrib import admin
from django.urls import include, path
from municipio_invest.api.core.urls import CORE_URLS

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include(CORE_URLS)),
    ]
