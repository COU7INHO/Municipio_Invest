# urls.py
from django.urls import re_path
from .views import MunicipalityView, ContractsView, MunicipalitiesView

CORE_URLS = [
    re_path(r'^api/municipality/$', MunicipalityView.as_view(), name='municipality'),
    re_path(r'^api/municipalities/$', MunicipalitiesView.as_view(), name='list_municipalities'),
    re_path(r'^api/municipality/contracts/$', ContractsView.as_view(), name='contracts')
]