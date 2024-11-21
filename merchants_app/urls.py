
from django.contrib import admin
from django.urls import path, include
from .views import *
from django.conf.urls import handler404

handler404 = custom_404_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('login/', login_view, name='login'),
    path('login/<str:username>/', login_view, name='login_user'),
    path('logout/', logout_view, name='logout'),
    path('transactions/<int:id>/', transaction_details,
         name='transaction_details'),
    path('search/', search, name='search'),
    path('search_results/', search_results, name='search_results'),
    path('transactions/<int:id>/delete/', delete_transaction,
         name='delete_transaction'),
    path('transactions/<int:id>/edit/', edit_transaction,
         name='edit_transaction'),

    path('customers/', customer_list, name='customer_list'),
    path('customers/<int:pk>/', customer_details, name='customer_details'),
    path('customers/add/', add_customer, name='add_customer'),
    path('customers/edit/<int:pk>/', edit_customer, name='edit_customer'),
    path('customers/delete/<int:pk>/', delete_customer, name='delete_customer'),


    path('transactions/', transactions_page, name='transactions_page'),


    path('credit-management/', credit_management, name='credit_management'),
    path('credit-management/<int:pk>/',
         mark_credit_paid, name='mark_credit_paid'),
]
