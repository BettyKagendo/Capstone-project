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

#define BinarySearchTree
class BinarySearchTree:
    def __init__(self):
        self.root = None
    
     #insert method
    def insert(self, product):
        if self.root is None:
            self.root = Node(product)
        else:
            self._insert_recursive (product, self.root)

    def _insert_recursive(self, product, node):
            if product.product_id < node.product.product_id:
                if node.left is None:
                    node.left = Node(product)
                else:
                    self._insert_recursive(product, node.left)
            elif product.product_id > node.product.product_id:
                if node.right is None:
                    node.right = Node(product)
                else:
                    self._insert_recursive(product, node.right)
     #search method
    def search(self, product_id):
        return self._search(product_id, self.root)

    def _search(self, product_id, node):
        if node is None:
            return None
        elif node.product.product_id == product_id:
            return node.product
        elif product_id < node.product.product_id:
            return self._search(product_id, node.left)
        else:
            return self._search(product_id, node.right)
        
    # Inorder Traversal
    def inorder_traversal(self):
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node, result):
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.product)
            self._inorder_recursive(node.right, result)

    
    # Preorder Traversal
    def preorder_traversal(self):
        result = []
        self._preorder_recursive(self.root, result)
        return result

    def _preorder_recursive(self, node, result):
        if node:
            result.append(node.product)
            self._preorder_recursive(node.left, result)
            self._preorder_recursive(node.right, result)

# Postorder Traversal
    def postorder_traversal(self):
        result = []
        self._postorder_recursive(self.root, result)
        return result

    def _postorder_recursive(self, node, result):
        if node:
            self._postorder_recursive(node.left, result)
            self._postorder_recursive(node.right, result)
            result.append(node.product)

