
from random import randint
import sqlite3
import os
import sys

DIR = os.path.dirname(os.path.abspath(__file__)) # Get the directory
DB_DIR = DIR + "/db" # Get the database directory
DB_PATH = DB_DIR + "/order.db" # Get the database file

# SQL queries
SHOW_TABLES = "SELECT name FROM sqlite_master WHERE type='table'"
CREATE_PRODUCT = "CREATE TABLE Product(name varchar(20), brand varchar(20), price int, PRIMARY KEY(brand, name))"
CREATE_STORE = "CREATE TABLE Store(id varchar(4) PRIMARY KEY, name varchar(20), address varchar(10) UNIQUE)"
CREATE_WAREHOUSE = "CREATE TABLE Warehouse(id varchar(4) PRIMARY KEY, name varchar(20), address varchar(10) UNIQUE)"
CREATE_SELLS = "CREATE TABLE Sells(product_name varchar(20), product_brand varchar(20), store_id varchar(4), quantity int, PRIMARY KEY(product_brand, product_name, store_id), FOREIGN KEY(product_brand, product_name) REFERENCES Product(brand, name), FOREIGN KEY(store_id) REFERENCES Store(id))"
CREATE_OWNS = "CREATE TABLE Owns(product_name varchar(20), product_brand varchar(20), warehouse_id varchar(4), quantity int, PRIMARY KEY(product_brand, product_name, warehouse_id), FOREIGN KEY(product_brand, product_name) REFERENCES Product(brand, name), FOREIGN KEY(warehouse_id) REFERENCES Warehouse(id))"
SELECT_PRODUCT = "SELECT * FROM Product"
SELECT_STORE = "SELECT * FROM Store"
SELECT_WAREHOUSE = "SELECT * FROM Warehouse"
SELECT_OWNS = "SELECT product_brand, product_name, quantity FROM Owns WHERE warehouse_id=?"
SELECT_SELLS = "SELECT product_brand, product_name, quantity FROM Sells WHERE store_id=?"
ADD_WAREHOUSE = "INSERT INTO Warehouse VALUES(?, ?, ?)"
DELETE_WAREHOUSE = "DELETE FROM Warehouse WHERE id=?"
ADD_OWNS = "INSERT INTO Owns VALUES(?, ?, ?, ?)"
UPDATE_OWNS = "UPDATE Owns SET quantity=? WHERE (product_name, product_brand, warehouse_id) = (?, ?, ?)"
DELETE_OWNS = "DELETE FROM Owns WHERE (product_name, product_brand, warehouse_id) = (?, ?, ?)"
DELETE_ALL_OWNS = "DELETE FROM Owns WHERE warehouse_id=?"
ADD_STORE = "INSERT INTO Store VALUES(?, ?, ?)"
DELETE_STORE = "DELETE FROM Store WHERE id=?"
ADD_SELLS = "INSERT INTO SELLS VALUES(?, ?, ?, ?)"
UPDATE_SELLS = "UPDATE Sells SET quantity=? WHERE (product_name, product_brand, store_id) = (?, ?, ?)"
DELETE_SELLS = "DELETE FROM Sells WHERE (product_name, product_brand, store_id) = (?, ?, ?)"
DELETE_ALL_SELLS = "DELETE FROM Sells WHERE store_id=?"
ADD_PRODUCT = "INSERT INTO Product VALUES (?, ?, ?)"
DELETE_PRODUCT = "DELETE FROM Product WHERE (name, brand) = (?, ?)"
DELETE_PD_FR_SELLS = "DELETE FROM Sells WHERE product_name=? AND product_brand=?"
DELETE_PD_FR_OWNS = "DELETE FROM Owns WHERE product_name=? AND product_brand=?"
UPDATE_PRICE = "UPDATE Product SET price=? WHERE (name, brand) = (?, ?)"

# If the database directory does not exist, create it
if not os.path.exists(DB_DIR):
    os.mkdir(DB_DIR)

# If the database file does not exist, create it
if not os.path.exists(DB_PATH):
    with open(DB_PATH, 'w'):
        pass

# Create database instance with the database file
sql = sqlite3.connect(DB_PATH)

# Create the SQL cursor
cursor = sql.cursor()

# Get the database tables
cursor.execute(SHOW_TABLES)
tables = cursor.fetchall()

# If the database tables are not valid, drop the database and recreate all the tables
if len(tables) != 5 or ('Store',) not in tables or ('Product',) not in tables or ('Warehouse',) not in tables or ('Sells',) not in tables or ('Owns',) not in tables:
    with open(DB_PATH, 'w'): pass # Overwrite the db file
    cursor.execute(CREATE_STORE)
    cursor.execute(CREATE_WAREHOUSE)
    cursor.execute(CREATE_PRODUCT)
    cursor.execute(CREATE_SELLS)
    cursor.execute(CREATE_OWNS)
    sql.commit()

# Main program loop
while True:
    # Print the option table
    print("\nWelcome to Order Admin Panel!")
    print("----------------------------------")
    print(" 1) List Warehouses")
    print(" 2) List Stocks of A Warehouse")
    print(" 3) Add Warehouse")
    print(" 4) Delete Warehouse")
    print(" 5) Add Product to Warehouse Stock")
    print(" 6) Remove Product from Warehouse Stock")
    print(" 7) List Stores")
    print(" 8) List Stocks of A Store")
    print(" 9) Add Store")
    print("10) Delete Store")
    print("11) Add Product to Store Stock")
    print("12) Remove Product from Store Stock")
    print("13) List Products")
    print("14) Add Product")
    print("15) Delete Product")
    print("16) Update Product Price")
    print("17) Exit\n")

    # Loop until the user enters a valid option
    while True:
        # Get the input
        raw_input = input("Please select a command: ")

        # If it is not integer, continue
        try:
            inp = int(raw_input)
        except:
            print("Invalid option.")
            continue
        
        # If the given integer not in the boundaries of the options, continue
        if inp < 1 or inp > 17:
            print("Invalid option.")
            continue
        
        # Break if it is valid
        break

    # Option 1 / List Warehouses
    if inp == 1:
        # Get warehouses
        cursor.execute(SELECT_WAREHOUSE)
        whs = cursor.fetchall()

        # Print warehouses
        print()
        for i in whs:
            print("{} #{}, (x,y)={}".format(i[1], i[0], i[2]))
        continue

    # Option 2 / List Stocks of A Warehouse
    if inp == 2:
        # Print warehouses label
        print()
        print("Warehouses:")
        cursor.execute(SELECT_WAREHOUSE)
        whs = cursor.fetchall()

        # Gather warehouse IDs in a list and print warehouses
        ids = []
        for i in whs:
            ids.append(i[0])
            print("{} #{}".format(i[1], i[0], i[2]))
        print()

        # Loop until the user enters a valid input
        while True:
            # Get an ID from the user
            id = input("Please enter the warehouse ID: ").strip()
            # If the given ID not in the IDs list, continue
            if id not in ids:
                print("Incorrect ID.")
                continue
            # Break if the ID is valid
            break
        
        # Get the products that the warehouse with the ID owns
        cursor.execute(SELECT_OWNS, (id,))
        pds = cursor.fetchall()

        # Print products
        print()
        for i in pds:
            print("Brand: {}, Name: {}, Qty: {}".format(i[0], i[1], i[2]))
        continue
    
    # Option 3 / Add Warehouse
    if inp == 3:
        # Get warehouses
        cursor.execute(SELECT_WAREHOUSE)
        whs = cursor.fetchall()

        # List for holding used addresses 
        used_addresses = []
        # List for holding used IDs
        ids = []

        # Gather addresses and IDs of warehouses
        for i in whs:
            ids.append(i[0])
            used_addresses.append(i[2])

        # Get stores
        cursor.execute(SELECT_STORE)
        sts = cursor.fetchall()

        # Gather addresses and IDs of stores
        for i in sts:
            ids.append(i[0])
            used_addresses.append(i[2])

        # Get a name
        print()
        name = input("Name: ").strip()

        # Print used addresses
        print("Used Addresses: {}".format(", ".join(used_addresses)))

        # Loop until the user enters a valid input
        while True:
            # Loop until the user enters a valid x
            while True:
                # Get x as string
                x_str = input("x: ").strip()

                # Try to convert it to integer, continue if cannot convert
                try:
                    x = int(x_str)
                except:
                    print("Invalid x-coordinate.")
                    continue
                
                # If the given x is not in bounds, continue
                if x < 0 or x > 9:
                    print("Invalid x-coordinate. Must be between 0 and 9.")
                    continue
                
                # Break if the x is valid
                break
            
            # Loop until the user enter a valid y
            while True:
                # Get the y as string
                y_str = input("y: ").strip()

                # Try to convert it to integer, continue if cannot convert
                try:
                    y = int(y_str)
                except:
                    print("Invalid y-coordinate.")
                    continue
                
                # If the given y is not in bounds, continue
                if y < 0 or y > 9:
                    print("Invalid y-coordinate. Must be between 0 and 9.")
                    continue
                
                # Break if the y is valid
                break
            
            # Check if there is a warehouse with the given x and y addresses, it there is, continue
            found = False
            for i in whs:
                if i[2] == "({},{})".format(x,y):
                    print("Invalid x and y. Both must be unique.")
                    found = True
                    break
            if found:
                continue
            
            # Check if there is a store with the given x and y addresses, it there is, continue
            for i in sts:
                if i[2] == "({},{})".format(x,y):
                    print("Invalid x and y. Both must be unique.")
                    found = True
                    break
            if found:
                continue
            
            # Break if the given address is valid
            break
        
        # Generate an unused ID
        while True:
            id = "{:04d}".format(randint(0,9999))

            if id not in ids:
                break
        
        # Insert warehouse into the database
        cursor.execute(ADD_WAREHOUSE, (id, name, "({},{})".format(x,y)))
        sql.commit()
        # Print success message
        print()
        print("{} #{} is created!".format(name, id))
        continue
    
    # Option 4 / Delete Warehouse
    if inp == 4:
        # Print warehouses label
        print()
        print("Warehouses:")

        # Get warehouses
        cursor.execute(SELECT_WAREHOUSE)
        whs = cursor.fetchall()

        # Gather warehouse IDs and print warehouses
        ids = []
        for i in whs:
            ids.append(i[0])
            print("{} #{}".format(i[1], i[0], i[2]))
        print()

        # Loop until the user enters a valid warehouse ID
        while True:
            # Get ID
            id = input("Enter warehouse ID: ").strip()

            # If the ID is not in IDs, continue
            if id not in ids:
                print("Invalid ID.")
                continue
            # Break if the ID is valid
            break
        
        # Delete warehouse stocks from database
        cursor.execute(DELETE_ALL_OWNS, (id,))
        sql.commit()
        # Delete warehouse from database
        cursor.execute(DELETE_WAREHOUSE, (id,))
        sql.commit()
        # Print success message
        print()
        print("Warehouse #{} is deleted!".format(id))
        continue
    
    # Option 5 / Add Product to Warehouse Stock
    if inp == 5:
        # Get all products
        cursor.execute(SELECT_PRODUCT)
        pds = cursor.fetchall()

        # List to hold product names and brands as tuples
        pd_tuples = []

        # Print products header
        print()
        print("Products:")

        # Add all the products as tuples to the list and print products
        for i in pds:
            pd_tuples.append((i[1], i[0]))
            print("Brand: {}, Name: {}, ${}".format(i[1], i[0], i[2]))
        print()

        # Loop until the user enters a valid product brand and name
        while True:
            # Get brand and name
            brand = input("Brand: ").strip()
            name = input("Name: ").strip()

            # If the brand and name not in tuples, continue
            if (brand,name) not in pd_tuples:
                print("Invalid product.")
                continue
            # Break if the product is valid
            break

        # Print warehouses header
        print()
        print("Warehouses:")

        # Get warehouses
        cursor.execute(SELECT_WAREHOUSE)
        whs = cursor.fetchall()

        # Gather warehouse IDs in a list and print warehouses
        ids = []
        for i in whs:
            ids.append(i[0])
            print("{} #{}".format(i[1], i[0], i[2]))
        print()

        # Loop until the user enters a valid warehouse ID
        while True:
            # Get ID
            id = input("Warehouse ID: ").strip()

            # If the ID is not in IDs list, continue
            if id not in ids:
                print("Invalid ID.")
                continue
            # Break if the ID is valid
            break
        
        # Loop until the user enters a valid quantity
        while True:
            # Get quantity as string
            qty_str = input("Quantity: ").strip()

            # Try to convert it to int, continue if cannot convert
            try:
                qty = int(qty_str)
            except:
                print("Invalid quantity.")
                continue
            
            # If quantity is below 1, continue
            if qty < 1:
                print("Invalid quantity. Cannot be less than 1.")
                continue
            
            # Break if the quantity is valid
            break
        
        # Get all the products that are already in the stock of the selected warehouse
        cursor.execute(SELECT_OWNS, (id,))
        owns = cursor.fetchall()

        # Variable for holding if the selected product is already in the stock
        found = False

        # Iterate over all the products in stock
        for i in owns:
            # If the product is in stock
            if i[0] == brand and i[1] == name:
                # Compute the new quantity
                new_qty = int(i[2]) + qty
                # Update the quantity
                cursor.execute(UPDATE_OWNS, (new_qty, name, brand, id))
                sql.commit()
                # Print success message
                print()
                print("{} stocks of {} {} is added to the stock of Warehouse #{}!".format(qty, brand, name, id))
                # Set variable as found
                found = True
                break
        
        # If the product is found, skip the rest of the block
        if found:
            continue
        
        # Add new product to the stock
        cursor.execute(ADD_OWNS, (name, brand, id, qty))
        sql.commit()
        # Print success message
        print()
        print("{} stocks of {} {} is added to the stock of Warehouse #{}!".format(qty, brand, name, id))
        continue
    
    # Option 6 / Remove Product from Warehouse Stock
    if inp == 6:
        # Print warehouses header
        print()
        print("Warehouses:")

        # Get warehouses
        cursor.execute(SELECT_WAREHOUSE)
        whs = cursor.fetchall()

        # Gather warehouse IDs in a list and print warehouses
        ids = []
        for i in whs:
            ids.append(i[0])
            print("{} #{}".format(i[1], i[0], i[2]))
        print()

        # Loop until the user enters a valid ID
        while True:
            # Get ID
            id = input("Warehouse ID: ").strip()

            # If the ID is not in the IDs list, continue
            if id not in ids:
                print("Invalid ID.")
                continue
            # Break if the ID is valid
            break

        # Get all the products in the selected warehouses's stock
        cursor.execute(SELECT_OWNS, (id,))
        in_stock = cursor.fetchall()

        # Print items in stock header
        print()
        print("Items in stock:")

        # Gather all the products as brand and name tuples, gather the quantities as values to the tuple keys, and print products
        pd_tuples = []
        qtys = {}
        for i in in_stock:
            pd_tuples.append((i[0], i[1]))
            qtys["({}, {})".format(i[0], i[1])] = int(i[2])
            print("Brand: {}, Name: {}, Qty: {}".format(i[0], i[1], i[2]))
        print()

        # Loop until the user enters a valid product brand and name
        while True:
            # Get brand and name
            brand = input("Brand: ").strip()
            name = input("Name: ").strip()

            # If the brand and name not in product tuples, continue
            if (brand,name) not in pd_tuples:
                print("Invalid product.")
                continue
            # Break if the product is valid
            break
        
        # Loop until the user enters a valid quantity
        while True:
            # Get quantity as string
            qty_str = input("Quantity: ").strip()

            # Try to convert it to int, continue if cannot convert
            try:
                qty = int(qty_str)
            except:
                print("Invalid quantity.")
                continue
            
            # If the given quantity is less than 0 or more than the total quantity of the product, continue
            if qty < 1 or qty > qtys["({}, {})".format(brand, name)]:
                print("Invalid quantity. Cannot be less than 1 or more than total quantity.")
                continue
            # Break if the quantity is valid
            break
        
        # If the total quantity - given quantity equals 0, delete the product from stock
        if qtys["({}, {})".format(brand, name)] - qty == 0:
            cursor.execute(DELETE_OWNS, (name, brand, id))
            sql.commit()
        # If there is still an amount quantity, update the quantity
        else:
            cursor.execute(UPDATE_OWNS, (qtys["({}, {})".format(brand, name)] - qty, name, brand, id))
            sql.commit()

        # Print success message
        print()
        print("{} stocks of {} {} is deleted from Warehouse #{}!".format(qty, brand, name, id))
        continue
    
    # Option 7 / List Stores
    if inp == 7:
        # Get stores
        cursor.execute(SELECT_STORE)
        sts = cursor.fetchall()

        # Print stores
        print()
        for i in sts:
            print("{} #{}, (x,y)={}".format(i[1], i[0], i[2]))
        continue
    
    # Option 8 / List Stocks of A Store
    if inp == 8:
        # Print stores label
        print()
        print("Stores:")
        cursor.execute(SELECT_STORE)
        sts = cursor.fetchall()

        # Gather store IDs in a list and print stores
        ids = []
        for i in sts:
            ids.append(i[0])
            print("{} #{}".format(i[1], i[0], i[2]))
        print()

        # Loop until the user enters a valid input
        while True:
            # Get an ID from the user
            id = input("Please enter the store ID: ").strip()
            # If the given ID not in the IDs list, continue
            if id not in ids:
                print("Incorrect ID.")
                continue
            # Break if the ID is valid
            break
        
        # Get the products that the store with the ID sells
        cursor.execute(SELECT_SELLS, (id,))
        pds = cursor.fetchall()

        # Print products
        print()
        for i in pds:
            print("Brand: {}, Name: {}, Qty: {}".format(i[0], i[1], i[2]))
        continue
    
    # Option 9 / Add Store
    if inp == 9:
        # Get warehouses
        cursor.execute(SELECT_WAREHOUSE)
        whs = cursor.fetchall()

        # List for holding used addresses 
        used_addresses = []
        # List for holding used IDs
        ids = []

        # Gather addresses and IDs of warehouses
        for i in whs:
            ids.append(i[0])
            used_addresses.append(i[2])

        # Get stores
        cursor.execute(SELECT_STORE)
        sts = cursor.fetchall()

        # Gather addresses and IDs of stores
        for i in sts:
            ids.append(i[0])
            used_addresses.append(i[2])

        # Get a name
        print()
        name = input("Name: ").strip()

        # Print used addresses
        print("Used Addresses: {}".format(", ".join(used_addresses)))

        # Loop until the user enters a valid input
        while True:
            # Loop until the user enters a valid x
            while True:
                # Get x as string
                x_str = input("x: ").strip()

                # Try to convert it to integer, continue if cannot convert
                try:
                    x = int(x_str)
                except:
                    print("Invalid x-coordinate.")
                    continue
                
                # If the given x is not in bounds, continue
                if x < 0 or x > 9:
                    print("Invalid x-coordinate. Must be between 0 and 9.")
                    continue
                
                # Break if the x is valid
                break
            
            # Loop until the user enter a valid y
            while True:
                # Get the y as string
                y_str = input("y: ").strip()

                # Try to convert it to integer, continue if cannot convert
                try:
                    y = int(y_str)
                except:
                    print("Invalid y-coordinate.")
                    continue
                
                # If the given y is not in bounds, continue
                if y < 0 or y > 9:
                    print("Invalid y-coordinate. Must be between 0 and 9.")
                    continue
                
                # Break if the y is valid
                break
            
            # Check if there is a warehouse with the given x and y addresses, it there is, continue
            found = False
            for i in whs:
                if i[2] == "({},{})".format(x,y):
                    print("Invalid x and y. Both must be unique.")
                    found = True
                    break
            if found:
                continue
            
            # Check if there is a store with the given x and y addresses, it there is, continue
            for i in sts:
                if i[2] == "({},{})".format(x,y):
                    print("Invalid x and y. Both must be unique.")
                    found = True
                    break
            if found:
                continue
            
            # Break if the given address is valid
            break
        
        # Generate an unused ID
        while True:
            id = "{:04d}".format(randint(0,9999))

            if id not in ids:
                break
        
        # Insert store into the database
        cursor.execute(ADD_STORE, (id, name, "({},{})".format(x,y)))
        sql.commit()
        # Print success message
        print()
        print("{} #{} is created!".format(name, id))
        continue
    
    # Option 10 / Delete Store
    if inp == 10:
        # Print stores label
        print()
        print("Stores:")

        # Get stores
        cursor.execute(SELECT_STORE)
        sts = cursor.fetchall()

        # Gather stores IDs and print stores
        ids = []
        for i in sts:
            ids.append(i[0])
            print("{} #{}".format(i[1], i[0], i[2]))
        print()

        # Loop until the user enters a valid store ID
        while True:
            # Get ID
            id = input("Enter store ID: ").strip()
            
            # If the ID is not in IDs, continue
            if id not in ids:
                print("Invalid ID.")
                continue
            # Break if the ID is valid
            break
            
        # Delete store stocks from database
        cursor.execute(DELETE_ALL_SELLS, (id,))
        sql.commit()
        # Delete store from database
        cursor.execute(DELETE_STORE, (id,))
        sql.commit()
        # Print success message
        print()
        print("Store #{} is deleted!".format(id))
        continue
    
    # Option 11 / Add Product to Store Stock
    if inp == 11:
        # Get all products
        cursor.execute(SELECT_PRODUCT)
        pds = cursor.fetchall()

        # List to hold product names and brands as tuples
        pd_tuples = []

        # Print products header
        print()
        print("Products:")

        # Add all the products as tuples to the list and print products
        for i in pds:
            pd_tuples.append((i[1], i[0]))
            print("Brand: {}, Name: {}, ${}".format(i[1], i[0], i[2]))
        print()

        # Loop until the user enters a valid product brand and name
        while True:
            # Get brand and name
            brand = input("Brand: ").strip()
            name = input("Name: ").strip()

            # If the brand and name not in tuples, continue
            if (brand,name) not in pd_tuples:
                print("Invalid product.")
                continue

            # Break if the product is valid
            break
        
        # Print stores header
        print()
        print("Stores:")

        # Get stores
        cursor.execute(SELECT_STORE)
        sts = cursor.fetchall()

        # Gather store IDs in a list and print stores
        ids = []
        for i in sts:
            ids.append(i[0])
            print("{} #{}".format(i[1], i[0], i[2]))
        print()

        # Loop until the user enters a valid store ID
        while True:
            # Get ID
            id = input("Store ID: ").strip()

            # If the ID is not in IDs list, continue
            if id not in ids:
                print("Invalid ID.")
                continue
            # Break if the ID is valid
            break
        
        # Loop until the user enters a valid quantity
        while True:
            # Get quantity as string
            qty_str = input("Quantity: ").strip()

            # Try to convert it to int, continue if cannot convert
            try:
                qty = int(qty_str)
            except:
                print("Invalid quantity.")
                continue
            
            # If quantity is below 1, continue
            if qty < 1:
                print("Invalid quantity. Cannot be less than 1.")
                continue
            
            # Break if the quantity is valid
            break
        
        # Get all the products that are already in the stock of the selected store
        cursor.execute(SELECT_SELLS, (id,))
        sells = cursor.fetchall()

        # Variable for holding if the selected product is already in the stock
        found = False

        # Iterate over all the products in stock
        for i in sells:
            # If the product is in stock
            if i[0] == brand and i[1] == name:
                # Compute the new quantity
                new_qty = int(i[2]) + qty
                # Update the quantity
                cursor.execute(UPDATE_SELLS, (new_qty, name, brand, id))
                sql.commit()
                # Print success message
                print()
                print("{} stocks of {} {} is added to the stock of Store #{}!".format(qty, brand, name, id))
                # Set variable as found
                found = True
                break
        
        # If the product is found, skip the rest of the block
        if found:
            continue
        
        # Add new product to the stock
        cursor.execute(ADD_SELLS, (name, brand, id, qty))
        sql.commit()
        # Print success message
        print()
        print("{} stocks of {} {} is added to the stock of Store #{}!".format(qty, brand, name, id))
        continue
    
    # Option 12 / Remove Product from Store Stock
    if inp == 12:
        # Print stores header
        print()
        print("Stores:")

        # Get stores
        cursor.execute(SELECT_STORE)
        sts = cursor.fetchall()

        # Gather store IDs in a list and print stores
        ids = []
        for i in sts:
            ids.append(i[0])
            print("{} #{}".format(i[1], i[0], i[2]))
        print()

        # Loop until the user enters a valid ID
        while True:
            # Get ID
            id = input("Store ID: ").strip()

            # If the ID is not in the IDs list, continue
            if id not in ids:
                print("Invalid ID.")
                continue
            break
        
        # Get all the products in the selected store's stock
        cursor.execute(SELECT_SELLS, (id,))
        in_stock = cursor.fetchall()

        # Print items in stock header
        print()
        print("Items in stock:")

        # Gather all the products as brand and name tuples, gather the quantities as values to the tuple keys, and print products
        pd_tuples = []
        qtys = {}
        for i in in_stock:
            pd_tuples.append((i[0], i[1]))
            qtys["({}, {})".format(i[0], i[1])] = int(i[2])
            print("Brand: {}, Name: {}, Qty: {}".format(i[0], i[1], i[2]))
        print()

        # Loop until the user enters a valid product brand and name
        while True:
            # Get brand and name
            brand = input("Brand: ").strip()
            name = input("Name: ").strip()

            # If the brand and name not in product tuples, continue
            if (brand,name) not in pd_tuples:
                print("Invalid product.")
                continue
            # Break if the product is valid
            break

        # Loop until the user enters a valid quantity
        while True:
            # Get quantity as string
            qty_str = input("Quantity: ").strip()

            # Try to convert it to int, continue if cannot convert
            try:
                qty = int(qty_str)
            except:
                print("Invalid quantity.")
                continue

            # If the given quantity is less than 0 or more than the total quantity of the product, continue
            if qty < 1 or qty > qtys["({}, {})".format(brand, name)]:
                print("Invalid quantity. Cannot be less than 1 or more than total quantity.")
                continue
            # Break if the quantity is valid
            break

        # If the total quantity - given quantity equals 0, delete the product from stock
        if qtys["({}, {})".format(brand, name)] - qty == 0:
            cursor.execute(DELETE_SELLS, (name, brand, id))
            sql.commit()
        # If there is still an amount quantity, update the quantity
        else:
            cursor.execute(UPDATE_SELLS, (qtys["({}, {})".format(brand, name)] - qty, name, brand, id))
            sql.commit()

        # Print success message
        print()
        print("{} stocks of {} {} is deleted from Store #{}!".format(qty, brand, name, id))
        continue
    
    # Option 13 / List Products
    if inp == 13:
        # Get products
        cursor.execute(SELECT_PRODUCT)
        pds = cursor.fetchall()

        # Print products
        print()
        for i in pds:
            print("Brand: {}, Name: {}, ${}".format(i[1], i[0], i[2]))
        continue
    
    # Option 14 / Add Product
    if inp == 14:
        # Print products header
        print()
        print("Products:")

        # Get products
        cursor.execute(SELECT_PRODUCT)
        pds = cursor.fetchall()

        # Gather all the products as brand and name tuples and print products
        tuples = []
        for i in pds:
            tuples.append((i[1], i[0]))
            print("Brand:{}, Name: {}".format(i[1], i[0]))
        print()

        # Loop until the user enters a valid product brand and name
        while True:
            # Get brand and name
            brand = input("Brand: ").strip()
            name = input("Name: ").strip()

            # If the brand and name not in product tuples, continue
            if (brand,name) in tuples:
                print("Product exists.")
                continue

            # Break if the product is valid
            break

        # Loop until the user enters a valid price
        while True:
            # Get price as string
            pr_str = input("Price: ").strip()

            # Try to convert it to int, continue if cannot convert
            try:
                price = int(pr_str)
            except:
                print("Invalid price.")
                continue

            # If the given price is less than 1, continue
            if price < 1:
                print("Invalid price. Cannot be less than 1.")
                continue
            
            # Break if the price is valid
            break
        
        # Add product
        cursor.execute(ADD_PRODUCT, (name, brand, price))
        sql.commit()
        # Print success message
        print()
        print("{} {} with the price ${} is added!".format(brand, name, price))
        continue

    # Option 15 / Delete Product
    if inp == 15:
        # Print products header
        print()
        print("Products:")

        # Get products
        cursor.execute(SELECT_PRODUCT)
        pds = cursor.fetchall()

        # Gather all the products as brand and name tuples and print products
        tuples = []
        for i in pds:
            tuples.append((i[1], i[0]))
            print("Brand:{}, Name: {}".format(i[1], i[0]))
        print()

        # Loop until the user enters a valid product brand and name
        while True:
            # Get brand and name
            brand = input("Brand: ").strip()
            name = input("Name: ").strip()

            # If the brand and name not in product tuples, continue
            if (brand,name) not in tuples:
                print("Product does not exist.")
                continue

            # Break if the product is valid
            break
        
        # Delete product from store stocks
        cursor.execute(DELETE_PD_FR_SELLS, (name, brand))
        sql.commit()
        # Delete product from warehouse stocks
        cursor.execute(DELETE_PD_FR_OWNS, (name, brand))
        sql.commit()
        # Delete product
        cursor.execute(DELETE_PRODUCT, (name, brand))
        sql.commit()
        # Print success message
        print()
        print("{} {} is deleted!".format(brand, name))
        continue
    
    # Option 16 / Update Product Price
    if inp == 16:
        # Print products header
        print()
        print("Products:")

        # Get products
        cursor.execute(SELECT_PRODUCT)
        pds = cursor.fetchall()

        # Gather all the products as brand and name tuples and print products
        tuples = []
        for i in pds:
            tuples.append((i[1], i[0]))
            print("Brand: {}, Name: {}, ${}".format(i[1], i[0], i[2]))
        print()

        # Loop until the user enters a valid product brand and name
        while True:
            # Get brand and name
            brand = input("Brand: ").strip()
            name = input("Name: ").strip()

            # If the brand and name not in product tuples, continue
            if (brand,name) not in tuples:
                print("Product does not exist.")
                continue

            # Break if the product is valid
            break
        
        # Loop until the user enters a valid price
        while True:
            # Get price as string
            pr_str = input("Price: ").strip()

            # Try to convert it to int, continue if cannot convert
            try:
                price = int(pr_str)
            except:
                print("Invalid price.")
                continue
            
            # If the given price is less than 1, continue
            if price < 1:
                print("Invalid price. Cannot be less than 1.")
                continue
            
            # Break if the price is valid
            break
        
        # Update product
        cursor.execute(UPDATE_PRICE, (price, name, brand))
        sql.commit()
        # Print success message
        print()
        print("Price of {} {} is changed to {}!".format(brand, name, price))
        continue
    
    # Option 17 / Exit
    if inp == 17:
        # Exit the system
        sys.exit(0)