import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


#establish a connection
try:
    conn = psycopg2.connect(
       dbname = os.getenv('database'),
       user = os.getenv('username'),
       password = os.getenv('password'),
       host = os.getenv('hostname')
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
        return f" Product ID: {self.product_id}, Name: {self.product_name}, Price: ${self.price:.2f}, Quantity:{self.quantity}"   


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
            self._insert_recursive (self.root, product)

    def _insert_recursive(self, node, product):
            if product.product_id < node.product.product_id:
                if node.left is None:
                    node.left = Node(product)
                    self._insert_into_database(product)  # Insert the product into the database
                else:
                    self._insert_recursive( node.left, product)
            elif product.product_id > node.product.product_id:
                if node.right is None:
                    node.right = Node(product)
                    self._insert_into_database(product)  # Insert the product into the database
                else:
                    self._insert_recursive(node.right, product)
            else:
                return #if the product_id already exists, do nothing
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
    
     # Delete method
    def delete(self, product_id):
        self.root = self._delete_recursive(product_id, self.root)

    def _delete_recursive(self, product_id, node):
        if node is None:
            return None

        if product_id < node.product.product_id:
            node.left = self._delete_recursive(product_id, node.left)
        elif product_id > node.product.product_id:
            node.right = self._delete_recursive(product_id, node.right)
        else:
            if node.left is None:
                temp = node.right #create a temporary ref to the right of the node to delete
                node = None #remove the node to delete
                return temp  
            elif node.right is None:
                temp = node.left
                node = None
                return temp
            #when node to be deleted has both a left and right child
            temp = self._max_value_node(node.right)
            node.product = temp.product
            node.right = self._delete_recursive(temp.product.product_id, node.right) #to delete the node we promoted to avoid duplication

        return node
    
    def _max_value_node(self, node):
        current = node
        while current.right is not None:
         current = current.right
        return current
        
    
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

# Insert a product into the database
    def _insert_into_database(self, product):
        cur = conn.cursor()
        query = "INSERT INTO fruitproducts (product_id, product_name, price, quantity) VALUES (%s, %s, %s, %s)"
        values = (product.product_id, product.product_name, product.price, product.quantity)
        try:
            cur.execute(query, values)
            conn.commit()
        except psycopg2.errors.UniqueViolation:
            #if the product already exists, do nothing
            conn.rollback()  #undo any changes made during the current database transaction
        except Exception as e: 
            print(f'Error: {e}')
            conn.rollback()
        finally: #to ensure that the cursor is always closed
            cur.close()


# Function to fetch data from the database and insert into the binary search tree
def populate_bst(bst):
    cur = conn.cursor()
    cur.execute("SELECT * FROM fruitproducts")
    rows = cur.fetchall()

    # Print each row in a separate line
    for row in rows:
        #print (row)  # This line prints each row fetched from the database
        product_id, product_name, price, quantity = row
        product = Product(product_id, product_name, float(price), quantity)
        bst.insert(product)
        #print(f"Inserted: {product}") 
    cur.close()
    return bst 


# Function to display the user menu
def display_menu():
    print("===== Product Management System =====")
    print("1. Insert a new product")
    print("2. Search for a product")
    print("3. Delete a product")
    print("4. Display products (Inorder Traversal)")
    print("5. Display products (Preorder Traversal)")
    print("6. Display products (Postorder Traversal)")
    print("0. Exit")

    # Function to get user input for a new product
def get_product_input():
    product_id = int(input("Enter the product ID: "))
    product_name = input("Enter the product name: ")
    price = float(input("Enter the price: "))
    quantity = int(input("Enter the quantity: "))
    return Product(product_id, product_name, price, quantity)


# Main program
bst = BinarySearchTree()  # create an instance of BinarySearchTree
populate_bst(bst)  # populate the BST with data from the database

while True:
    display_menu()
    choice = input("Enter your choice: ")

    if choice == "1":
        product = get_product_input()
        bst.insert(product)
        print("Product inserted successfully.")

    elif choice == "2":
        product_id = int(input("Enter the product ID to search: "))
        product = bst.search(product_id)
        if product:
            print("Product found:")
            print(product)
        else:
            print("Product not found.")

    elif choice == "3":
        product_id = int(input("Enter the product ID to delete: "))
        bst.delete(product_id)
        print("Product deleted successfully.")

    elif choice == "4":
        print("Products (Inorder Traversal):")
        for product in bst.inorder_traversal():
            print(product)

    elif choice == "5":
        print("Products (Preorder Traversal):")
        for product in bst.preorder_traversal():
            print(product)

    elif choice == "6":
        print("Products (Postorder Traversal):")
        for product in bst.postorder_traversal():
            print(product)

    elif choice == "0":
        print("Exiting the program.")
        break
    else:
        print("Invalid choice. Please try again.")
        

    
