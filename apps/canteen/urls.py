from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('become_canteen/', views.become_canteen, name='become_canteen'),
    path('canteen_admin/', views.canteen_admin, name='canteen_admin'),
    path('add_product/', views.add_product, name='add_product'),
    path('edit_canteen/', views.edit_canteen, name='edit_canteen'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='canteen/login.html'), name='login'),
    path('', views.canteens, name='canteens'),
    path('<int:canteen_id>/',views.canteen, name='canteen'),
]
