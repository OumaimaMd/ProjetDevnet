from django.urls import path
from . import views
from .views import CustomLoginView
from .views import custom_login
urlpatterns = [
    path('', views.accueil, name='accueil'),  # Page d'accueil
    path('home/', views.home, name='home'),  
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('cours/<int:course_id>/', views.course_detail, name='course_detail'),
    path('course/<int:course_id>/upload/', views.upload_resource, name='upload_resource'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('a_propos/', views.a_propos, name='a_propos'),
    path('upload_resource/<int:course_id>/', views.upload_resource, name='upload_resource'),
    path('reserver/', views.select_subject, name='select_subject'),
    path('reserver/<str:subject>/', views.select_year, name='select_year'),
    path('reserve/<int:course_id>/', views.reserve_course, name='reserve_course'),
     path('dashboard/add/', views.add_course, name='add_course'),
    path('courses/', views.course_list, name='course_list'),
     path('login/', custom_login, name='login'),
    path('courses/edit/<int:course_id>/', views.edit_course, name='edit_course'),  
    path('courses/delete/<int:course_id>/', views.delete_course, name='delete_course'),
    path('edit/<int:course_id>/', views.edit_course_page, name='edit_course_page'),
     
]   
