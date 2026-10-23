import json

class Product:
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

    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    def to_dictionary(self):
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock
        }

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

        for product in self.products:
            print(
                f"ID: {product.get_product_id()} | "
                f"Name: {product.get_name()} | "
                f"Price: ${product.get_price():.2f} | "
                f"Stock: {product.get_stock()}"
            )

        print("--------------------------------")

INVENTORY_FILE = "inventory.json"

def load_inventory():
    inventory = Inventory()

    try:
        with open(INVENTORY_FILE, "r") as file:
            data = json.load(file)

        for item in data:
            product = Product(
                item["id"],
                item["name"],
                item["price"],
                item["stock"]
            )

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

            product_id = input("Product ID: ")
            product_name = input("Product Name: ")
            price = float(input("Price: "))
            stock = int(input("Stock Quantity: "))

            product = Product(
                product_id,
                product_name,
                price,
                stock
            )

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

                new_stock = int(
                    input("New Stock Quantity: ")
                )

                product.update_stock(new_stock)

                print("\nStock updated successfully!")

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