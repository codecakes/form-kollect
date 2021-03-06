from django.urls import path
from form_kollect.apps.designer import views

urlpatterns = [
    path("index/", views.FormList.as_view(), name="designer-index"),
    path("create/", views.create, name="designer-create"),
    path("create_bulk_forms/", views.create_bulk_forms, name="designer-bulk-forms"),
    path("show-bulk-forms/", views.show_bulk_forms, name="designer-show-bulk-forms"),
]
