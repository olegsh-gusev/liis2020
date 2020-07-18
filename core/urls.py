from .views import register, vacant_space, reservation_info, reservation
from django.urls import path

app_name = "core"
# app_name will help us do a reverse look-up latter.

urlpatterns = [
    path('register/', register),
    path('vacant_space/', vacant_space),
    path('reservation/', reservation),
    path('reservation_info/', reservation_info),
    #    path('reservation_info/<int:workplace_id>/', reservation_info)

]
