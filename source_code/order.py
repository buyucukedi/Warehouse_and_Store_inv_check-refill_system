
from tkinter import *
from tkinter import messagebox
from lib.product import Product
from lib.store import Store
from lib.warehouse import Warehouse
import os
import sqlite3

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

# Method for initializing the database
def init_db():
    global cursor
    global sql

    # If the database directory does not exist, create it
    if not os.path.exists(DB_DIR):
        os.mkdir(DB_DIR)

    # If the database file does not exist, create it
    if not os.path.exists(DB_PATH):
        with open(DB_PATH, 'w'): pass

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

# Method for initializing the screen
def init_screen():
    global stores
    global products
    
    # Initiliaze the main screen
    main_screen = Tk()
    main_screen.resizable(False, False)
    main_screen.title("Order")

    # Initialize the left frame
    left_frame = Frame(main_screen, borderwidth=5, relief="groove")
    left_frame.grid(row=0,column=0,padx=10,pady=10)

    # Initialize the rigth frame
    right_frame = Frame(main_screen, borderwidth=5, relief="groove")
    right_frame.grid(row=0,column=1,padx=10,pady=10)

    global store_stock_var
    global product_var
    global quantity_var
    global store_var

    # Variable for product dropdown menu selection
    product_var = StringVar()

    # If the value of product_var changes, run variable check
    product_var.trace("w", lambda name, index, mode, sv=product_var: var_check())

    # Variable for quantity entry
    quantity_var = IntVar()

    # If the value of quantity_var changes, run variable check
    quantity_var.trace("w", lambda name, index, mode, sv=quantity_var: var_check())

    # Variable for store dropdown menu selection
    store_var = StringVar()

    # If the value of store_var changes, run variable check
    store_var.trace("w", lambda name, index, mode, sv=store_var: var_check())

    # Variable for store stock dropdown menu selection
    store_stock_var = StringVar()

    # If the value of store_stock_var changes, change the contents of listbox
    store_stock_var.trace("w", lambda name, index, mode, sv=store_stock_var: update_stocks())

    # "Product to be delivered:" label
    product_label = Label(left_frame, text="Product to be delivered:")
    product_label.grid(row=0,column=0,sticky=N+S+W,padx=10,pady=3)

    # Product dropdown menu
    global product_dd
    product_dd = OptionMenu(left_frame, product_var, *products)
    product_dd.grid(row=1,column=0,sticky=NSEW,padx=10,pady=3)

    # "Quantity:" label
    quantity_label = Label(left_frame, text="Quantity:")
    quantity_label.grid(row=2,column=0,sticky=N+S+W,padx=10,pady=3)

    # Quantity entry
    global quantity_entry
    quantity_entry = Entry(left_frame, textvariable=quantity_var,width=40)
    quantity_entry.grid(row=3,column=0,sticky=NSEW,padx=10,pady=3)

    # "Store to be delivered to:" label
    store_label = Label(left_frame, text="Store to be delivered to:")
    store_label.grid(row=4,column=0,sticky=N+S+W,padx=10,pady=3)

    # Store dropdown menu
    global store_dd
    store_dd = OptionMenu(left_frame, store_var, *stores)
    store_dd.grid(row=5,column=0,sticky=NSEW,padx=10,pady=3)

    # "Order Now" button
    global order_button
    order_button = Button(left_frame, text="Order Now!",command=deliver,state=DISABLED)
    order_button.grid(row=6,column=0,sticky=NSEW,padx=10,pady=11)

    # "Check the stocks of:" label
    store_stock_label = Label(right_frame, text="Check the stocks of:")
    store_stock_label.grid(row=0,column=0,sticky=N+S+W,padx=10,pady=3)

    # Store stocks dropdown menu
    global store_stock_dd
    store_stock_dd = OptionMenu(right_frame, store_stock_var, *stores)
    store_stock_dd.grid(row=1,column=0,sticky=NSEW,padx=10,pady=3)
    
    # Stock listbox
    global stocks
    stocks = Listbox(right_frame, exportselection=False,height=9,width=40,state=DISABLED)
    stocks.grid(row=2,column=0,rowspan=5,sticky=NSEW,padx=10,pady=8)

    # Start the main screen loop
    main_screen.mainloop()

# Method for updating the listbox to ch<nge its contents based on he
def update_stocks():
    global store_stock_var
    global stocks
    global stores

    # Get the selected store
    store_name = store_stock_var.get()

    # Enable the listbox and delete its contents
    stocks.configure(state=NORMAL)
    stocks.delete(0, END)

    # If nothing is selected, disable the listbox again and return
    if store_name == "":
        stocks.configure(state=DISABLED)
        return
    
    # Iterate over all stores
    for i in stores:
        # If the selected store is the current one
        if str(i) == store_name:
            # Add all the stocks to the listbox
            for j in i.in_stock:
                stocks.insert(END, "{}, Qty: {}".format(j[0], j[1]))

            # Disable the listbox again and return
            stocks.configure(state=DISABLED)
            return

# Method for checking the variables for being valid
def var_check():
    global order_button
    global product_var
    global quantity_var
    global store_var

    # Try to get the quantity, if the entered value is not integer, it will raise an exception
    try:
        qty = quantity_var.get()
    # If an exception occurs, disable the button and return
    except:
        order_button.configure(state=DISABLED)
        return

    # If the variables are empty or not valid, disable the button
    if qty <= 0 or store_var.get() == "" or product_var.get() == "":
        order_button.configure(state=DISABLED)
    # Otherwise, enable the button
    else:
        order_button.configure(state=NORMAL)

# Method for delivering a product to a store
def deliver():
    global product_var
    global quantity_var
    global store_var
    global store_stock_var
    global products
    global stores
    global warehouses
    global product_dd
    global quantity_entry
    global store_dd
    global store_stock_dd

    # Disable all the input elements
    product_dd.configure(state=DISABLED)
    quantity_entry.configure(state=DISABLED)
    store_dd.configure(state=DISABLED)
    store_stock_dd.configure(state=DISABLED)

    # Get the input values
    qty = quantity_var.get()
    product_str = product_var.get()
    store_str = store_var.get()

    # Select the store
    for i in stores:
        if str(i) == store_str:
            store = i
            break
    
    # List to hold all the warehouses that have the desired amount of stocks of the product
    has_stock = []

    # For holding the desired product
    product = None

    # Iterate over all warehouses
    for i in warehouses:
        # Iterate over the products in stock on the current warehouse
        for j in i.in_stock:
            # If the desired product is in stock
            if str(j[0]) == product_str and j[1] >= qty:
                # Select the product if it is not selected before
                if product == None:
                    product = j[0]
                # Add the warehouse to the list of warehouses that have stocks
                has_stock.append(i)

    # If there is no warehouse that has the desired amount of stocks, show an error message, reset and enable all the input elements, and return
    if len(has_stock) == 0:
        messagebox.showerror("Out of Stock", "There is no warehouse with such a stock of the desired product.")
        product_dd.configure(state=NORMAL)
        quantity_entry.configure(state=NORMAL)
        store_dd.configure(state=NORMAL)
        store_stock_dd.configure(state=NORMAL)
        product_var.set("")
        store_var.set("")
        quantity_var.set(0)
        return

    # Initialize the minimum distance
    min_dist = float("inf")

    # Initliaze the minimum-distanced warehouse
    min_dist_wh = None

    # Iterate over all the warehouses that have stocks
    for i in has_stock:
        # If the distance between store and the current warehouse is less than the last minimum disttance
        if abs(((store.x - i.x)**2 + (store.y - i.y)**2)**(1/2)) < min_dist:
            # Update the distance and the minimum-distanced warehouse
            min_dist = abs(((store.x - i.x)**2 + (store.y - i.y)**2)**(1/2))
            min_dist_wh = i

    # Deliver the desired amount of stocks of the product from the minimum-distanced warehouse to the selected store
    min_dist_wh.deliver(store, product, qty, stores, warehouses, cursor, sql)
    # Select the store to the stock check
    store_stock_var.set(store_str)
    # Update the listbox
    update_stocks()
    # Enable and reset all the input elements
    product_dd.configure(state=NORMAL)
    quantity_entry.configure(state=NORMAL)
    store_dd.configure(state=NORMAL)
    store_stock_dd.configure(state=NORMAL)
    product_var.set("")
    store_var.set("")
    quantity_var.set(0)

# Method for getting values from database
def get_from_db():
    global sql
    global cursor
    global products
    global warehouses
    global stores

    # Initialize the lists
    products = []
    warehouses = []
    stores = []

    # Get all the products fro database
    cursor.execute(SELECT_PRODUCT)
    pds = cursor.fetchall()

    # Add the products to the products list
    for i in pds:
        products.append(Product(i[0], i[1], i[2]))

    # If there is no product, add an empty string to the list
    if len(products) == 0:
        products.append("")

    # Get all the stores from database
    cursor.execute(SELECT_STORE)
    sts = cursor.fetchall()
    
    # Iterate over all stores in database
    for i in sts:
        # Get all the products that the store sells
        cursor.execute(SELECT_SELLS, (i[0],))
        pds_stock = cursor.fetchall()

        # Create a list to hold the products in stock
        stock = []

        # Iterate over all products that the store sells on database
        for j in pds_stock:
            # Find the product
            for k in products:
                if j[0] == k.brand and j[1] == k.name:
                    # Add the product and its quantity to the store stock list
                    stock.append([k, j[2]])
                    break
        
        # Get the x and y coordinates of the store from database
        x = int(i[2].lstrip("(").rstrip(")").split(",")[0])
        y = int(i[2].lstrip("(").rstrip(")").split(",")[1])

        # Add the store with all its values to the stores list
        stores.append(Store(x, y, i[1], stock, i[0]))

    # If there is no store, add an empty string to the list
    if len(stores) == 0:
        stores.append("")

    # Get all the warehouses from database
    cursor.execute(SELECT_WAREHOUSE)
    whs = cursor.fetchall()
    
    # Iterate over all warehouses
    for i in whs:
        # Get all the products that the warehouse owns
        cursor.execute(SELECT_OWNS, (i[0],))
        pds_stock = cursor.fetchall()

        # Create a list to hold the products in stock
        stock = []

        # Iterate over all products that the warehouse owns on database
        for j in pds_stock:
            # Find the product
            for k in products:
                # Add the product and its quantity to the warehouse stock list
                if j[0] == k.brand and j[1] == k.name:
                    stock.append([k, j[2]])
                    break
        
        # Get the x and y coordinates of the warehouse from database
        x = int(i[2].lstrip("(").rstrip(")").split(",")[0])
        y = int(i[2].lstrip("(").rstrip(")").split(",")[1])

        # Add the warehouse with all its values to the warehouses list
        warehouses.append(Warehouse(x, y, i[1], stock, i[0]))

    # If there is no warehouse, add an empty string to the list
    if len(warehouses) == 0:
        warehouses.append("")

# If the script run directly
if __name__ == '__main__':
    init_db() # Initlialize database
    get_from_db() # Get values from database
    init_screen() # Initialize the GUI
