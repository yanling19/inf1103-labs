MAX_CAPACITY = 500
TAX_RATE = 0.1
INVENTORY_FILE = "inventory.txt"

def get_valid_input():
    while True:
        product_name = input("Enter Product Name (type 'quit' to stop): ")
        if product_name.lower() == 'quit':
            return "quit"

        product_quantity = input("Enter Product Quantity: ")
        
        if not product_quantity.isdigit():
            print("Invalid input. Please enter a valid number.")
            return None

        product_quantity = int(product_quantity)

        if product_quantity < 0:
            print("Product quantity cannot be negative. Please enter a valid number.")
            return None

        else:
            return product_name, product_quantity

def process_delivery(current_total, new_value):
    new_total = current_total + new_value
    return new_total

def calculate_tax(amount):
    tax = amount * TAX_RATE
    return tax

def generate_report(total_units, failed_attempts):
    print("Total Units Processed:", total_units)
    print("Number of Failed/Rejected Entries:", failed_attempts)

def load_inventory():
    try:
        with open(INVENTORY_FILE, "r") as file:
            lines = file.readlines()

            inventory = int(lines[0].strip())
            transaction_history = []

            for line in lines[1:]:
                transaction_history.append(line.strip())
        return inventory, transaction_history
    except FileNotFoundError:
        return 0, []

def save_inventory(inventory, transaction_history):
    with open(INVENTORY_FILE, "w") as file:
        file.write(str(inventory) + "\n")
        for transaction in transaction_history:
            file.write(transaction + "\n")

def main():
    inventory, transaction_history = load_inventory()
    failed_entries = 0
    total_deliveries = 0
    tax_amount = 0
    exit_program = False

    print("Current Orders:")
    for transaction in transaction_history:
        print(transaction)

    while not exit_program:
        audit = get_valid_input()
        if audit == "quit":
            save_inventory(inventory, transaction_history)
            print("Order successfully saved to inventory.txt")
            exit_program = True

        elif audit is None:
            failed_entries += 1

        else:
            product_name, product_quantity = audit
            if transaction_history:
                last_transaction = transaction_history[-1]
                transaction_number = int(last_transaction.split(",")[0]) + 1
            else:
                transaction_number = 1001

            new_transaction = f"{transaction_number}, {product_name}, {product_quantity}"
            transaction_history.append(new_transaction)
            inventory = process_delivery(inventory, product_quantity)
            total_deliveries += 1
            tax = calculate_tax(product_quantity)
            tax_amount += tax
            print("New Order Added:")
            print(new_transaction)

            if inventory > MAX_CAPACITY:
                print("Warning: Inventory exceeds maximum capacity of 500 units.")
                exit_program = True



if __name__ == "__main__":
    main()