from django.urls import path

from . import views

app_name = "vlogs"
urlpatterns = [
    path("", views.vlog_list, name="list"),
    path("vlogs/new/", views.vlog_create, name="create"),
    path("vlogs/<int:pk>/", views.vlog_detail, name="detail"),
    path("vlogs/<int:pk>/edit/", views.vlog_update, name="update"),
    path("vlogs/<int:pk>/delete/", views.vlog_delete, name="delete"),
]
