import json
from abc import ABC, abstractmethod

class CanBeShipped(ABC):

    @abstractmethod
    def calculate_shipping_cost(self):
        pass

class Supplier:
    def __init__(self, supplier_id: str, name: str, contact_email: str):
        self.__supplier_id: str = supplier_id
        self.__name: str = name
        self.__contact_email: str = contact_email
 
    def get_supplier_id(self) -> str:
        return self.__supplier_id
 
    def get_name(self) -> str:
        return self.__name
 
    def get_contact_email(self) -> str:
        return self.__contact_email
 
    def display_information(self) -> None:
        print(f"Supplier ID: {self.__supplier_id}")
        print(f"Supplier Name: {self.__name}")
        print(f"Supplier Email: {self.__contact_email}")
 
    def to_dictionary(self) -> dict:
        return {
            "id": self.__supplier_id,
            "name": self.__name,
            "contact_email": self.__contact_email
        }

class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, supplier: Supplier):
        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = price
        self.__stock: int = stock
        self.__supplier: Supplier = supplier  # association (reference only)
 
    def update_stock(self, quantity: int) -> None:
        self.__stock = quantity
 
    def display_information(self) -> None:
        print(f"ID: {self.__product_id}")
        print(f"Name: {self.__name}")
        print(f"Price: ${self.__price:.2f}")
        print(f"Stock: {self.__stock}")
        self.__supplier.display_information()
 
    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass
 
    def get_product_id(self) -> str:
        return self.__product_id
 
    def get_name(self) -> str:
        return self.__name
 
    def get_price(self) -> float:
        return self.__price
 
    def get_stock(self) -> int:
        return self.__stock
 
    def get_supplier(self) -> Supplier:
        return self.__supplier
 
    @abstractmethod
    def to_dictionary(self) -> dict:
        pass

class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, supplier: Supplier, weight: float):
        super().__init__(product_id, name, price, stock, supplier)
        self.__weight: float = weight
 
    def display_information(self) -> None:
        super().display_information()
        print(f"Weight: {self.__weight:.2f} kg")
        # Shipping is part of how a physical product describes itself, so
        # callers never need isinstance() to decide whether to print it.
        print(f"Shipping Cost: ${self.calculate_shipping_cost():.2f}")
 
    def get_fulfilment_info(self) -> str:
        return "This product requires physical shipping"
 
    def calculate_shipping_cost(self) -> float:
        return 5.00 + (self.__weight * 2.00)
 
    def to_dictionary(self) -> dict:
        return {
            "type": "physical",
            "id": self.get_product_id(),
            "name": self.get_name(),
            "price": self.get_price(),
            "stock": self.get_stock(),
            "supplier": self.get_supplier().to_dictionary(),
            "weight": self.__weight
        }

class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, supplier: Supplier, download_size: float):
        super().__init__(product_id, name, price, stock, supplier)
        self.__download_size: float = download_size
 
    def display_information(self) -> None:
        super().display_information()
        print(f"Download Size: {self.__download_size:.2f} MB")
 
    def get_fulfilment_info(self) -> str:
        return "This product is delivered digitally"
 
    def to_dictionary(self) -> dict:
        return {
            "type": "digital",
            "id": self.get_product_id(),
            "name": self.get_name(),
            "price": self.get_price(),
            "stock": self.get_stock(),
            "supplier": self.get_supplier().to_dictionary(),
            "download_size": self.__download_size
        }

class Inventory:
    def __init__(self):
        # Typed with the base class so any Product subclass can be stored.
        self.products: list[Product] = []
 
    def add_product(self, product: Product) -> bool:
        if self.find_product(product.get_product_id()) is not None:
            return False
 
        self.products.append(product)
        return True
 
    def remove_product(self, product_id: str) -> bool:
        """Remove the reference only. The Product object itself lives on."""
        product = self.find_product(product_id)
 
        if product is None:
            return False
 
        self.products.remove(product)
        return True
 
    def find_product(self, product_id: str) -> Product | None:
        for product in self.products:
            if product.get_product_id() == product_id:
                return product
 
        return None
 
    def display_all(self) -> None:
        print("\nCurrent Inventory")
        print("--------------------------------")
 
        if not self.products:
            print("No products in inventory.")
 
        # Polymorphism / LSP: works on the Product abstraction only.
        for product in self.products:
            product.display_information()
            print(f"Fulfilment: {product.get_fulfilment_info()}")
            print("--------------------------------")

class OrderLine:
    def __init__(self, product: Product, quantity: int):
        self.__product: Product = product
        self.__quantity: int = quantity
 
    def get_product(self) -> Product:
        return self.__product
 
    def get_quantity(self) -> int:
        return self.__quantity
 
    def calculate_subtotal(self) -> float:
        return self.__product.get_price() * self.__quantity
 
    def display_information(self) -> None:
        print(f"{self.__product.get_name()} "
              f"(ID: {self.__product.get_product_id()}) "
              f"x {self.__quantity} = ${self.calculate_subtotal():.2f}")
 
 
class Order:
    def __init__(self, order_id: str):
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []
 
    def get_order_id(self) -> str:
        return self.__order_id
 
    def get_order_lines(self) -> list[OrderLine]:
        return list(self.__order_lines)  # copy so lines can't be managed outside
 
    def add_order_line(self, product: Product, quantity: int) -> None:
        # The Order creates its own OrderLine (composition).
        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)
 
    def remove_order_line(self, product_id: str) -> bool:
        for order_line in self.__order_lines:
            if order_line.get_product().get_product_id() == product_id:
                self.__order_lines.remove(order_line)
                return True
 
        return False
 
    def calculate_total(self) -> float:
        total = 0.0
 
        for order_line in self.__order_lines:
            total += order_line.calculate_subtotal()
 
        return total
 
    def display_information(self) -> None:
        print(f"\nOrder ID: {self.__order_id}")
        print("--------------------------------")
 
        if not self.__order_lines:
            print("No order lines.")
 
        for order_line in self.__order_lines:
            order_line.display_information()
 
        print("--------------------------------")
        print(f"Order Total: ${self.calculate_total():.2f}")

INVENTORY_FILE = "inventory.json"

UNKNOWN_SUPPLIER_ID = "UNKNOWN"

def load_inventory() -> tuple[Inventory, str]:
    inventory = Inventory()
    # Suppliers are shared between products, so create each one only once.
    suppliers: dict[str, Supplier] = {}
 
    try:
        with open(INVENTORY_FILE, "r") as file:
            data = json.load(file)
 
        for item in data:
            product_type = item.get("type", "physical")
 
            # Older files have no supplier, so fall back to a placeholder.
            supplier_data = item.get("supplier", {})
            supplier_id = supplier_data.get("id", UNKNOWN_SUPPLIER_ID)
 
            if supplier_id not in suppliers:
                suppliers[supplier_id] = Supplier(
                    supplier_id,
                    supplier_data.get("name", "Unknown Supplier"),
                    supplier_data.get("contact_email", "N/A")
                )
 
            supplier = suppliers[supplier_id]
 
            if product_type == "physical":
                product = PhysicalProduct(
                    item["id"],
                    item["name"],
                    item["price"],
                    item["stock"],
                    supplier,
                    item.get("weight", 0.0)
                )
            elif product_type == "digital":
                product = DigitalProduct(
                    item["id"],
                    item["name"],
                    item["price"],
                    item["stock"],
                    supplier,
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
 
 
def save_inventory(inventory: Inventory) -> None:
    data = []
 
    for product in inventory.products:
        data.append(product.to_dictionary())
 
    with open(INVENTORY_FILE, "w") as file:
        json.dump(data, file, indent=4)
 
    print("Inventory saved successfully.")
 
 
def get_or_create_supplier(inventory: Inventory) -> Supplier:
    """Reuse an existing supplier with the same ID, otherwise create one."""
    supplier_id = input("Supplier ID: ")
 
    for product in inventory.products:
        existing = product.get_supplier()
        if existing.get_supplier_id() == supplier_id:
            print(f"Using existing supplier: {existing.get_name()}")
            return existing
 
    supplier_name = input("Supplier Name: ")
    contact_email = input("Supplier Contact Email: ")
 
    return Supplier(supplier_id, supplier_name, contact_email)
 
 
def show_product_details(product: Product) -> None:
    """Works for any Product subclass without modification (LSP)."""
    product.display_information()
    print(f"Fulfilment: {product.get_fulfilment_info()}")
 
 
def create_order(inventory: Inventory) -> Order | None:
    order_id = input("Order ID: ")
    order = Order(order_id)
 
    print("Add products to the order (leave Product ID blank to finish).")
 
    while True:
        product_id = input("\nProduct ID: ")
 
        if product_id == "":
            break
 
        product = inventory.find_product(product_id)
 
        if product is None:
            print("Product not found.")
            continue
 
        try:
            quantity = int(input("Quantity: "))
        except ValueError:
            print("Invalid input. Enter a valid integer for quantity.")
            continue
 
        if quantity <= 0:
            print("Quantity must be greater than zero.")
            continue
 
        order.add_order_line(product, quantity)
        print("Order line added.")
 
    if not order.get_order_lines():
        print("\nNo order lines added. Order discarded.")
        return None
 
    return order
 
 
def main() -> None:
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
        print("5. Remove Product")
        print("6. Create Order")
        print("7. Save Inventory")
        print("8. Exit")
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
 
                supplier = get_or_create_supplier(inventory)
 
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
                        supplier,
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
                        supplier,
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
 
            product = inventory.find_product(product_id)
 
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
 
            product = inventory.find_product(product_id)
 
            if product is not None:
 
                print("\nProduct Found:")
                print("----------------------")
                show_product_details(product)
                print("----------------------")
 
            else:
                print("\nProduct not found.")
 
        elif option == "5":
            print("\nRemove Product")
 
            product_id = input("Enter Product ID: ")
 
            if inventory.remove_product(product_id):
                print("\nProduct removed from inventory.")
            else:
                print("\nProduct not found.")
 
        elif option == "6":
            print("\nCreate Order")
 
            order = create_order(inventory)
 
            if order is not None:
                order.display_information()
 
        elif option == "7":
            print("\nSaving inventory...")
            save_inventory(inventory)
 
        elif option == "8":
            print("\nSaving inventory before exit...")
            save_inventory(inventory)
 
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.\n")
 
            exit_program = True
 
        else:
            print("\nInvalid option. Please try again.")
 
 
if __name__ == "__main__":
    main()