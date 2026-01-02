from django.urls import path

from . import views

app_name = "datahub"

urlpatterns = [
    path("", views.index, name="index"),
    path("delete/<int:record_id>/", views.delete, name="delete"),
    path("add", views.add, name="add"),
    path("api/data", views.api_data, name="api_data"),
    path("api/add", views.api_add, name="api_add"),
    path("api/data/<int:record_id>", views.api_delete, name="api_delete"),
]
