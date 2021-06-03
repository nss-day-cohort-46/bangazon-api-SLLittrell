"""Module for generating users that have favorited a seller """
from bangazon_reports.views.connections import Connection
import sqlite3
from django.shortcuts import render
from bangazonapi.models import Product


def inexpensive_product_list(request):
    """Function to build an HTML report of games by user"""
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
            SELECT p.* 
            FROM bangazonapi_product p
            WHERE p.price <= 999.00
            GROUP BY p.price
            ORDER BY p.price DESC
            """)

            dataset = db_cursor.fetchall()


            inexpensive_products = []

            for row in dataset:
                product = {
                    'id':row['id'],
                    'price':row['price'],
                    'product_name':row['name'],
                    'quantity':row['quantity']
                }

                
                inexpensive_products.append(product)
                
            list_of_inexpensive_products = list(inexpensive_products)
        # Specify the Django template and provide data context
        template = 'products/inexpensive_products.html'
        context = {
            'inexpensive_product_list': list_of_inexpensive_products
        }

        return render(request, template, context)