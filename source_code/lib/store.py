
from random import randint
import lib.stddraw as std
from lib.picture import Picture
from pathlib import Path

# SQL queries
ADD_STOCK = "INSERT INTO Sells VALUES(?, ?, ?, ?)"
UPDATE_STOCK = "UPDATE Sells SET quantity=? WHERE (product_name, product_brand, store_id) = (?, ?, ?)"

# Store class
class Store:
    # Initialize a store with x, y, and its name. Optionally, products in stock and ID can be given.    
    def __init__(self, x, y, name, in_stock=None, id="{:04d}".format(randint(0,9999))) -> None:
        # Set the fields
        self.id =id
        self.name = name
        self.x = x
        self.y = y
        
        # Set the in_stock field
        if in_stock is None:
            self.in_stock = []
        else:
            self.in_stock = in_stock

    # Return a formatted string of the store
    def __str__(self) -> str:
        return "{} #{}".format(self.name, self.id)

    # Add a desired amount of quantity of the given product to the stock
    def add_stock(self, product, quantity, cursor, sql):
        # Iterate over all products in stock
        for i in self.in_stock:
            # If the given product is in the stock already
            if i[0].name == product.name and i[0].brand == product.brand:
                # Update its quantity both on list and database
                i[1] += quantity
                cursor.execute(UPDATE_STOCK, (i[1], product.name, product.brand, self.id))
                sql.commit()
                return

        # If the given product is a new product, add it both to list and database
        cursor.execute(ADD_STOCK, (product.name, product.brand, self.id, quantity))
        sql.commit()
        self.in_stock.append([product, quantity])

    # Draw the stock
    def draw(self):
        # Get the picture and place it onto the canvas
        std.picture(Picture(Path(__file__).parent.resolve().parent.resolve().joinpath("src", "store.png")),self.x+0.5, self.y+0.5)
        # Write its name and ID on top of the warehouse
        std.setPenColor(std.BLACK)
        std.setFontSize(10)
        std.text(self.x+0.5,self.y+1.15,str(self))
