"""Module for generating users that have favorited a seller """
from bangazon_reports.views.connections import Connection
import sqlite3
from django.shortcuts import render
from bangazonapi.models import Customer, Favorite


def user_favorited_list(request):
    """Function to build an HTML report of games by user"""
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
               SELECT
                    favorite_id,
                    seller_name,
                    customer,
                    cu.first_name|| '' || cu.last_name customer_name
                FROM (Select 
					f.id favorite_id,
                    f.seller_id,
                    f.customer_id customer,
                    u.first_name|| '' || u.last_name seller_name
                FROM bangazonapi_favorite f
                JOIN auth_user u ON f.seller_id == u.id)
                JOIN auth_user cu ON customer == cu.id
            """)

            dataset = db_cursor.fetchall()


            user_favorited = {}

            for row in dataset:
                user = {
                    'id':row['favorite_id'],
                    'seller':row['seller_name']
                }

                u_id =row['customer']

                if u_id in user_favorited:
                    user_favorited[u_id]['favorited'].append(user)
                else:
                    user_favorited[u_id] = {
                        "id": u_id,
                        "customer_name": row["customer_name"],
                        "favorited": [user]
                    }
            list_of_users_with_favorited = list(user_favorited.values())
        # Specify the Django template and provide data context
        template = 'users/users_favorited.html'
        context = {
            'user_favorited_list': list_of_users_with_favorited
        }

        return render(request, template, context)
