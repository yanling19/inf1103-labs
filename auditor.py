inventory = 0
failed_entries = 0

while True:
    stock = input("Enter stock quantity (type 'quit' to stop): ")

    if stock.lower() == 'quit':
        break

    elif not stock.isdigit():
        print("Invalid input. Please enter a valid number.")
        failed_entries += 1
        continue

    elif int(stock) < 0:
        print("Stock quantity cannot be negative. Please enter a valid number.")
        failed_entries += 1
        continue

    else:
        stock = int(stock)
        inventory += stock
        print(f"Current inventory: {inventory}")

        if inventory > 500:
            print("Warning: Inventory exceeds maximum capacity of 500 units.")
            break
print(f"Total Units Processed: {inventory}")
print(f"Number of Failed/Rejected Entries: {failed_entries}")
