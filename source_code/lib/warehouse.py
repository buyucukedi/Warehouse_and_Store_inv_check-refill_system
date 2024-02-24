
from random import randint
import lib.stddraw as std
from lib.picture import Picture
from pathlib import Path

# SQL queries
DELETE_STOCK = "DELETE FROM Owns WHERE (product_name, product_brand, warehouse_id) = (?, ?, ?)"
UPDATE_STOCK = "UPDATE Owns SET quantity=? WHERE (product_name, product_brand, warehouse_id) = (?, ?, ?)"

# Warehouse class
class Warehouse:
    # Initialize a warehouse with x, y, and its name. Optionally, products in stock and ID can be given.
    def __init__(self, x, y, name, in_stock=None, id="{:04d}".format(randint(0,9999))) -> None:
        # Set the fields
        self.id = id
        self.name = name
        self.x = x
        self.y = y
        
        # Set the in_stock field
        if in_stock is None:
            self.in_stock = []
        else:
            self.in_stock = in_stock

    # Return a formatted string of the warehouse
    def __str__(self) -> str:
        return "{} #{}".format(self.name, self.id)

    # Draw the warehouse
    def draw(self):
        # Get the picture and place it onto the canvas
        std.picture(Picture(Path(__file__).parent.resolve().parent.resolve().joinpath("src", "warehouse.png")),self.x+0.5, self.y+0.5)
        # Write its name and ID on top of the warehouse
        std.setPenColor(std.BLACK)
        std.setFontSize(10)
        std.text(self.x+0.5,self.y+1.15,str(self))

    # Remove a desired amount of quantity of the given product from the stock
    def remove_stock(self, product, quantity, cursor, sql):
        # Iterate over all the products in stock
        for i in self.in_stock:
            # If the current product is the given one
            if str(i[0]) == str(product):
                # If the product quantity will be zero after the removing operating, remove the product directly both from list and database
                if i[1] - quantity == 0:
                    self.in_stock.remove(i)
                    cursor.execute(DELETE_STOCK, (product.name, product.brand, self.id))
                    sql.commit()
                # If there will be more than 0 stocks left, update the quantity both on list and database
                else:
                    i[1] -= quantity
                    cursor.execute(UPDATE_STOCK, (i[1], product.name, product.brand, self.id))
                    sql.commit()
                break

    # Draw a road from this warehouse to the given store
    def _draw_road(self, store, delivered=False):
        # Get the distance
        dist = round(((store.x - self.x)**2 + (store.y - self.y)**2)**(1/2))
        # Compute the step count
        step_count = dist * 3
        # Compute the x and y step values
        x_step = (store.x - self.x) / step_count
        y_step = (store.y - self.y) / step_count
        # Set the pen color
        # If the product is not delivered yet, set it to red. Otherwise, set it to green.
        if not delivered:
            std.setPenColor(std.RED)
        else:
            std.setPenColor(std.DARK_GREEN)

        # For every step
        for i in range(step_count):
            # Draw a circle for the step
            std.filledCircle(self.x + 0.5 + x_step*i, self.y + 0.5 + y_step*i, 0.1)
            # If not delivered yet, wait for a random amount of time between 0.4 and 1.2 second.
            if not delivered:
                std.show(randint(400,1200))

    # Deliver an amount of stocks of a product from this warehouse to the given store
    def deliver(self, store, product, quantity, stores_list, warehouses_list, cursor, sql):
        # Create a canvas
        std.setCanvasSize(550, 600)
        std.setXscale(0,10)
        std.setYscale(0,11)
        
        # Draw the stores
        for i in stores_list:
            i.draw()

        # Draw the warehouses
        for i in warehouses_list:
            i.draw()

        # Set the font family, font size, color
        std.setFontFamily("arial")
        std.setFontSize(20)
        std.setPenColor(std.BLACK)

        # Draw the "Preparing items..." text on top of the canvas
        std.boldText(5, 10.6, "Preparing items...")

        # Wait for a random amount of time which is based on the quantity
        std.show(randint(100, 600) * quantity)

        # Remove stocks of the product from this warehouse
        self.remove_stock(product, quantity, cursor, sql)
        # Add stocks of the product to the store
        store.add_stock(product, quantity, cursor, sql)

        # Clear the canvaas
        std.clear()

        # Draw the stores
        for i in stores_list:
            i.draw()

        # Draw the warehouses
        for i in warehouses_list:
            i.draw()

        # Set the font family, font size, color
        std.setFontFamily("arial")
        std.setFontSize(20)
        std.setPenColor(std.BLACK)

        # Draw the delivering statement text on top of the canvas
        std.boldText(5, 10.6, "Delivering from {} #{} to {} #{}...".format(self.name, self.id, store.name, store.id))

        # Draw a road between this warehouse and the store
        self._draw_road(store)

        # Clear the canvas
        std.clear()

        # Draw the stores
        for i in stores_list:
            i.draw()

        # Draw the warehouses
        for i in warehouses_list:
            i.draw()

        # Draw the delivered road
        self._draw_road(store, delivered=True)

        # Set the font family, font size, color
        std.setFontFamily("arial")
        std.setPenColor(std.DARK_GREEN)
        std.setFontSize(20)

        # Draw the "Delivered!" text on top of the canvas
        std.boldText(5, 10.6, "Delivered!")

        # Show the canvas and wait for 1.5 seconds
        std.show(1500)

        # Hide the canvas
        std.hide()