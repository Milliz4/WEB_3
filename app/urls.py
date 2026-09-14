from django.contrib import admin
from django.urls import path

from customers import views

urlpatterns = [
    path('', views.show_customers),
    path('admin/', admin.site.urls),
]
