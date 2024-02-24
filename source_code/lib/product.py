
# Product class
class Product:
    # Create a product with name, brand, and price.
    def __init__(self, name, brand, price) -> None:
        # Set the fields
        self.name = name
        self.brand = brand
        self.price = price

    # Return a formatted string of the product
    def __str__(self) -> str:
        return "{} {}, ${}".format(self.brand, self.name, self.price)