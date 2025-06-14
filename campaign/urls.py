from django.urls import path
from .import views
urlpatterns = [
    path("campaign/", views.campaign, name="campaign"),
    path("new-campaign/", views.new_campaign, name="new-campaign"),
]
