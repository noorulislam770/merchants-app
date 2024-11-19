from django.urls import path


from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add_transaction', views.add_transaction, name='add_transaction'),
    # path('search/', views.search, name='search'),

]
