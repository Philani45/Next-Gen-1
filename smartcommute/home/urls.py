from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('register/', views.register, name='register'),
    path('schedule/', views.schedule, name='schedule'),
    path('location/', views.location, name='location'),
    path('route/', views.route, name='route'),
    path('departure/', views.departure, name='departure'),
    path('notifications/', views.notifications, name='notifications'),
    path('settings/', views.settings, name='settings'),
    path('datastorage/', views.datastorage, name='datastorage'),
    path('login/', views.login, name='login'),
    path("add_schedule/", views.add_schedule, name="add_schedule"),
    path("auto-route/", views.auto_route, name="auto_route"),
    path("route/", views.route_view, name="route"),
    path('schedule/add/', views.add_schedule, name='add_schedule'),
    path('schedule/', views.edit_schedule, name='edit_schedule'),
    path('schedule/delete/<int:id>/', views.delete_schedule, name='delete_schedule')
]