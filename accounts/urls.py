from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/<int:id>/', views.user_profile, name='user_profile'),
    path('logout/', views.logout_view, name='logout'),
    path('user_list/', views.user_list, name='user_list'),
    path('delete_user/<int:id>/', views.delete_user, name='delete_user'),
    path('export_users_csv/', views.export_users_csv, name='export_users_csv'),
    

]