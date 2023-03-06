from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import (
    CustomLoginView,
    create_schema,
    delete_schema,
    generate_data,
    get_data_schema,
    get_data_schemas,
    root,
    update_schema,
)

urlpatterns = [
    path("", root, name="root"),
    path("schemas/", get_data_schemas, name="schema_list"),
    path("schemas/create/", create_schema, name="create_schema"),
    path("schemas/<int:pk>/", get_data_schema, name="schema"),
    path("schemas/<int:pk>/update/", update_schema, name="update_schema"),
    path("schemas/<int:pk>/delete/", delete_schema, name="delete_schema"),
    path("schemas/<int:pk>/generate/", generate_data, name="generate"),
    path("account/login/", CustomLoginView.as_view(), name="login"),
    path("account/logout/", LogoutView.as_view(), name="logout"),
]
