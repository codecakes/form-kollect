from django.urls import path
from form_kollect.apps.designer import views

urlpatterns = [
    path("index/", views.FormList.as_view(), name="designer-index"),
    path("create/", views.create, name="designer-create"),
    path("create_bulk_forms/", views.create_bulk_forms, name="designer-bulk-forms"),
    path("edit-bulk-forms/", views.edit_bulk_forms, name="designer-edit-bulk-forms"),
    # path("redirect-bulk-forms/", views.redirect_bulk_forms, name="redirect-bulk-forms"),
    path("add-form-options/", views.add_form_options, name="add-form-options",),
    path("view-bulk-form/", views.view_bulk_form, name="view-bulk-form"),
]
