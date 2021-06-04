  
from bangazon_reports.views.orders.incomplete_orders import incomplete_order_list
from bangazon_reports.views.orders.closed_orders import completed_order_list
from bangazon_reports.views.products.inexpensive_report import inexpensive_product_list
from bangazon_reports.views.products.expensive_report import expensive_product_list
from bangazon_reports.views.products.inexpensive_report import inexpensive_product_list
from django.urls import path

from .views.users.users_favorited import user_favorited_list

urlpatterns = [
    path('reports/user_favorited', user_favorited_list),
    path('reports/expensive_report', expensive_product_list),
    path('reports/inexpensive_report', inexpensive_product_list),
    path('reports/inexpensive_report', inexpensive_product_list),
    path('reports/completed_orders_report', completed_order_list),
    path('reports/incomplete_orders_report', incomplete_order_list),
]