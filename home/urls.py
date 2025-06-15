from django.urls import path
from .import views
urlpatterns = [
    path("", views.home, name="home"),
    path("privacy_policy/", views.privacy_policy, name="privacy_policy"),
    path("terms_and_condition/", views.terms_and_condition, name="terms_and_condition"),
]
