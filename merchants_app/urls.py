
from django.contrib import admin
from django.urls import path, include
from .views import login_view, logout_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
