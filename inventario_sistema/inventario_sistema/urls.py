"""
URL configuration for sistema_inventario project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# inventario_sistema/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from app.views import login_view  # Asegúrate de importar la vista adecuada

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', include('app.urls')),  # Verifica si necesitas esto aquí
    path('login/', include('app.urls')),     # Verifica si necesitas esto aquí
    path('home/', include('app.urls')),      # Verifica si necesitas esto aquí
    path('', include('app.urls')),           # Verifica si necesitas esto aquí
     path('', login_view, name='login'),  # Redirige la raíz a la vista home
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)