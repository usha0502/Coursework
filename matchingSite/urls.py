from django.urls import path
from django.views.generic import TemplateView
from . import views
from matchingSite import views

urlpatterns = [
    path('', views.index, name='index'),
	path('register/', views.register, name='register'),
    path('registerinfo/', views.registerinfo, name='registerinfo'),
    path('login/', views.login, name='login'),
    path('not_logged_in/', views.not_logged_in, name='not_logged_in'),
    path('matched_users/', views.matched_users, name='matched_users'),
    path('logout/', views.logout, name='logout'),
    path('navigation/', views.navigation, name='navigation'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('edit_profile_info/', views.edit_profile_info, name='edit_profile_info'),
    path('view_profile/', views.view_profile, name='view_profile'),
    path('view_profiles/', views.view_profiles, name='view_profiles'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('forgot_password_info/', views.forgot_password_info, name='forgot_password_info'),
    path('change_password/', views.change_password, name='change_password'),
    path('filter/', views.filter, name= 'filter'),
    path('fav/', views.fav, name='fav')
]
