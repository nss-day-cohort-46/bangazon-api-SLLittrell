"""Module for generating users that have favorited a seller """
from bangazon_reports.views.connections import Connection
import sqlite3
from django.shortcuts import render
from bangazonapi.models import Order


def completed_order_list(request):
    """Function to build an HTML report of games by user"""
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
            SELECT 
                u.first_name ||" "|| u.last_name customer_name,
                '$' || sum(pr.price) total_payed,
                o.id order_id,
                p.merchant_name payment
            FROM bangazonapi_order o
            JOIN bangazonapi_orderproduct op ON op.order_id == o.id
            JOIN bangazonapi_payment p ON p.id == o.payment_type_id
            JOIN bangazonapi_product pr ON pr.id == op.product_id
            JOIN bangazonapi_customer c ON c.id == o.customer_id
            JOIN auth_user u ON u.id == c.user_id
            WHERE o.payment_type_id IS NOT NULL
            GROUP BY order_id
            """)

            dataset = db_cursor.fetchall()


            closed_orders = []

            for row in dataset:
                closed = {
                    'order_id':row['order_id'],
                    'customer_name':row['customer_name'],
                    'total':row['total_payed'],
                    'payment_type': row['payment']
                }

                
                closed_orders.append(closed)
                
            list_of_closed_orders = list(closed_orders)
        # Specify the Django template and provide data context
        template = 'orders/complete_orders.html'
        context = {
            'completed_order_list': list_of_closed_orders
        }

        return render(request, template, context)