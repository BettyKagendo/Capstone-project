import psycopg2
from decouple import config

#establish a connection
try:
    conn = psycopg2.connect(
       dbname=config('database'),
       user='postgres',
       password=config('password'),
       host='localhost'
    )
    print ('Connected to the  database')
except psycopg2.Error as err:
    print ("Unable to connect to the database: ", err)  




    #define the product class
class Product:
    def __init__(self, product_id, product_name, price, quantity):
        self.product_id = product_id
        self.product_name = product_name
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return f"Product: {self.name}, Price: {self.price}, Quantity:{self.quantity}"   


#define the node class
class Node:
    def __init__(self, product):
        self.product = product
        self.left = None
        self.right = None                                                    