# app/urls.py

from django.urls import path
from .views import register_view, login_view, home, export_to_excel, edit_product,deactivate_product,export_to_excel_without_images,logout_view,my_view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('home/', home, name='home'),
    path('export_excel/', export_to_excel, name='export_excel'),
    path('export_excel_without_images/', export_to_excel_without_images, name='export_excel_without_images'),  
    path('edit/<int:pk>/', edit_product, name='edit_product'),
    path('deactivate_product/<int:product_id>/', deactivate_product, name='deactivate_product'),
    path('logout/', logout_view, name='logout'),
    path('protected/', my_view, name='protected'),
]