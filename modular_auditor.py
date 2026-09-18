MAX_CAPACITY = 500
TAX_RATE = 0.1

def get_valid_input():
    while True:
        stock = input("Enter stock quantity (type 'quit' to stop): ")
        if stock.lower() == 'quit':
            return "quit"
        
        elif not stock.isdigit():
            print("Invalid input. Please enter a valid number.")
            return None

        elif int(stock) < 0:
            print("Stock quantity cannot be negative. Please enter a valid number.")
            return None

        else:
            return int(stock)

def process_delivery(current_total, new_value):
    new_total = current_total + new_value

    print("Current inventory: ", current_total)
    print("New inventory: ", new_value)
    print("Total Units Processed: ", new_total)

    return new_total

def calculate_tax(amount):
    tax = amount * TAX_RATE
    print("Tax Rate for the current inventory: ", TAX_RATE)
    print("Tax Amount for current inventory: ", tax)
    return tax

def generate_report(total_units, failed_attempts):
    print("Total Units Processed:", total_units)
    print("Number of Failed/Rejected Entries:", failed_attempts)

def main():
    inventory = 0
    failed_entries = 0
    total_deliveries = 0
    exit_program = False

    while not exit_program:
        audit = get_valid_input()
        if audit == "quit":
            exit_program = True
        elif audit is None:
            failed_entries += 1
        else:
            inventory = process_delivery(inventory, audit)
            total_deliveries += 1
            tax = calculate_tax(inventory)

            if inventory > MAX_CAPACITY:
                print("Warning: Inventory exceeds maximum capacity of 500 units.")
                exit_program = True

    generate_report(inventory, failed_entries)

if __name__ == "__main__":
    main()


    



