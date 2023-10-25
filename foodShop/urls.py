from django.contrib import admin
from django.urls import include, path
from shop import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('shop.urls')),
    path('shop/', include('shop.urls')),
]
