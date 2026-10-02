import json
INVENTORY_FILE = "inventory.json"

def load_inventory():
    inventory = []

    try:
        with open(INVENTORY_FILE, "r") as file:
            inventory = json.load(file)

        status = "success"               
    
    except FileNotFoundError:
        status = "not found"
    
    return inventory, status

def save_inventory(inventory):
    with open(INVENTORY_FILE, "w") as file:
        json.dump(inventory, file, indent=4)
        print("Inventory saved successfully.")

def search_product(inventory, product_id):
    for product in inventory:
        if product["id"] == product_id:
            return product
        
    return None

def add_product(inventory, product_id, product_name, price, stock):
    if search_product(inventory, product_id) is not None:
        return False

    product = {
        "id": product_id,
        "name": product_name,
        "price": price,
        "stock": stock
    }

    inventory.append(product)
    return True

def update_stock(inventory, product_id, new_stock):
    product = search_product(inventory, product_id)

    if product is None:    
        return False

    product["stock"] = new_stock
    return True

def display_all(inventory):
    print("\nCurrent Inventory")
    print("-----------------------------")

    for product in inventory:
        print(f"ID:{product['id']}|"
              f"Name:{product['name']}|"
              f"Price:${product['price']:.2f}|"
              f"Stock:{product['stock']}"
        )

    print("--------------------------------")

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

    print("\n--------MENU--------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("--------------------")

    exit_program = False

    while not exit_program:
        option = input("\nEnter option: ")

        if option == "1":
            display_all(inventory)

        elif option == "2":
            print("\nAdd New Product")

            product_id = input("Product ID: ")
            product_name = input("Product Name: ")
            price = float(input("Price: "))
            stock = int(input("Stock Quantity: "))

            if add_product(inventory, product_id, product_name, price, stock):
                print("\nProduct added successfully!")
                save_inventory(inventory)
            else:
                print("\nProduct already exists.")

        elif option == "3":
            print("\nUpdate Stock")

            product_id = input("Enter Product ID: ")
            product = search_product(inventory, product_id)
            if product is not None:
                print("\nProduct Found")
                print("Name: ",product["name"])
                print("Current Stock: ",product["stock"])

                new_stock = int(input("New Stock Quantity: "))

                update_stock(inventory, product_id, new_stock)
                print("\nStock updated successfully!")
            else:
                print("\nProduct not found.")

        elif option == "4":
            print("\nSearch Product")

            product_id = input("Enter Product ID: ")
            product = search_product(inventory, product_id)

            if product is not None:
                print("\nProduct Found:")
                print("-----------------------------")
                print("ID: ",product["id"])
                print("Name: ",product["name"])
                print("Price: $",product["price"])
                print("Stock: ",product["stock"])
                print("-----------------------------")
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