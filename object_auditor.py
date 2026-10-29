import json
from abc import ABC, abstractmethod

class CanBeShipped(ABC):

    @abstractmethod
    def calculate_shipping_cost(self):
        pass

class Product(ABC):
    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    def update_stock(self, quantity):
        self.__stock = quantity

    def display_information(self):
        print(f"ID: {self.__product_id}")
        print(f"Name: {self.__name}")
        print(f"Price: ${self.__price:.2f}")
        print(f"Stock: {self.__stock}")

    @abstractmethod
    def get_fulfilment_info(self):
        pass

    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    @abstractmethod
    def to_dictionary(self):
        pass

class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self.__weight = weight

    def display_information(self):
        super().display_information()
        print(f"Weight: {self.__weight:.2f} kg")
    
    def get_fulfilment_info(self):
        return "This product requires physical shipping"
    
    def calculate_shipping_cost(self):
        return 5.00 + (self.__weight * 2.00)

    def to_dictionary(self):
        data = {
            "type": "physical",
            "id": self.get_product_id(),
            "name": self.get_name(),
            "price": self.get_price(),
            "stock": self.get_stock(),
            "weight": self.__weight
        }
        return data

class DigitalProduct(Product):
    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        self.__download_size = download_size

    def display_information(self):
        super().display_information()
        print(f"Download Size: {self.__download_size:.2f} MB")
    
    def get_fulfilment_info(self):
        return "This product is delivered digitally"
    
    def to_dictionary(self):
        data = {
            "type": "digital",
            "id": self.get_product_id(),
            "name": self.get_name(),
            "price": self.get_price(),
            "stock": self.get_stock(),
            "download_size": self.__download_size
        }
        return data

class Inventory:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        if self.search_product(product.get_product_id()) is not None:
            return False

        self.products.append(product)
        return True

    def search_product(self, product_id):
        for product in self.products:
            if product.get_product_id() == product_id:
                return product

        return None

    def display_all(self):
        print("\nCurrent Inventory")
        print("--------------------------------")

        if not self.products:
            print("No products in inventory.")

        for product in self.products:
            product.display_information()
            print(f"Fulfilment: {product.get_fulfilment_info()}")

        if isinstance(product, CanBeShipped):
            print(f"Shipping Cost: ${product.calculate_shipping_cost():.2f}")

        print("--------------------------------")

INVENTORY_FILE = "inventory.json"

def load_inventory():
    inventory = Inventory()

    try:
        with open(INVENTORY_FILE, "r") as file:
            data = json.load(file)

        for item in data:
            product_type = item.get("type", "physical")

            if product_type == "physical":
                product = PhysicalProduct(
                    item["id"],
                    item["name"],
                    item["price"],
                    item["stock"],
                    item.get("weight", 0.0)
                )
            elif product_type == "digital":
                product = DigitalProduct(
                    item["id"],
                    item["name"],
                    item["price"],
                    item["stock"],
                    item.get("download_size", 0.0)
                )
            else:
                print(f"Skipping product {item.get('id', 'unknown')}:"
                      f" Unknown product type '{product_type}'."
                )
                continue

            inventory.add_product(product)

        status = "success"

    except FileNotFoundError:
        status = "not found"

    return inventory, status

def save_inventory(inventory):
    data = []

    for product in inventory.products:
        data.append(product.to_dictionary())

    with open(INVENTORY_FILE, "w") as file:
        json.dump(data, file, indent=4)

    print("Inventory saved successfully.")

def main():
    print("====================================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("====================================")

    inventory, status = load_inventory()

    if status == "success":
        print("\ninventory.json found.")
        print("Inventory loaded successfully.")
    else:
        print("\ninventory.json not found.")
        print("Starting with an empty inventory.")

    exit_program = False

    while not exit_program:

        print("\n--------MENU--------")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Exit")
        print("--------------------")

        option = input("\nEnter option: ")

        if option == "1":
            inventory.display_all()

        elif option == "2":
            print("\nAdd New Product")
            print("1. Physical Product")
            print("2. Digital Product")

            product_type = input("Choose product type (1 or 2): ")

            if product_type not in ("1", "2"):
                print("\nInvalid product type.")
                continue

            product_id = input("Product ID: ")
            product_name = input("Product Name: ")

            try:
                price = float(input("Product Price: "))
                stock = int(input("Stock Quantity: "))

                if price < 0 or stock < 0:
                    print("\nPrice and stock must be non-negative.")
                    continue

                if product_type == "1":
                    weight = float(input("Product Weight (kg): "))

                    if weight < 0:
                        print("\nWeight must be non-negative.")
                        continue

                    product = PhysicalProduct(
                        product_id,
                        product_name,
                        price,
                        stock,
                        weight
                    )

                else:
                    download_size = float(input("Download Size (MB): "))

                    if download_size < 0:
                        print("\nDownload size must be non-negative.")
                        continue

                    product = DigitalProduct(
                        product_id,
                        product_name,
                        price,
                        stock,
                        download_size
                    )
            except ValueError:
                print("\nInvalid input. Enter valid numbers.")
                continue

            if inventory.add_product(product):
                print("\nProduct added successfully!")
            else:
                print("\nProduct already exists.")

        elif option == "3":
            print("\nUpdate Stock")

            product_id = input("Enter Product ID: ")

            product = inventory.search_product(product_id)

            if product is not None:

                print("\nProduct Found")
                print("Name:", product.get_name())
                print("Current Stock:", product.get_stock())

                try:
                    new_stock = int(
                        input("New Stock Quantity: ")
                    )

                    if new_stock < 0:
                        print("\nStock quantity must be non-negative.")
                        continue

                    product.update_stock(new_stock)
                    print("\nStock updated successfully!")

                except ValueError:
                    print("\nInvalid input. Enter a valid integer for stock quantity.")
                    continue

            else:
                print("\nProduct not found.")

        elif option == "4":
            print("\nSearch Product")

            product_id = input("Enter Product ID: ")

            product = inventory.search_product(product_id)

            if product is not None:

                print("\nProduct Found:")
                print("----------------------")
                product.display_information()
                print(f"Fulfilment: {product.get_fulfilment_info()}")

                if isinstance(product, CanBeShipped):
                    print(f"Shipping Cost: ${product.calculate_shipping_cost():.2f}")
                    
                print("----------------------")

            else:
                print("\nProduct not found.")

        elif option == "5":
            print("\nSaving inventory...")
            save_inventory(inventory)

        elif option == "6":
            print("\nSaving inventory before exit...")
            save_inventory(inventory)

            print("\nThank you for using Inventory Management System.")
            print("Program terminated.\n")

            exit_program = True

        else:
            print("\nInvalid option. Please try again.")

if __name__ == "__main__":
    main()