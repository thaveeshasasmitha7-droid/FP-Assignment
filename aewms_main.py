import os  
from datetime import datetime  # to take date and time

# Automated E-Waste Management System (AEWMS)

STORAGE_LIMIT_KG = 1000.0
WARNING_LEVEL = 0.80
BULK_DISCOUNT_LIMIT = 50.0
BULK_DISCOUNT_RATE = 0.05
HAZARD_LIMIT_DAYS = 30

# Data file saved directly to PC
DATA_FILE = "ewaste_data.txt"

ewaste_records = []

# File Handling

def load_data():
    """Load any existing saved record for the text file in PC."""

    global ewaste_records

    # If the file does not yet exist 
    if not os.path.exists(DATA_FILE):
        ewaste_records = []
        return
    
    try:
        with open(DATA_FILE, "r") as file:
            lines = file.readlines()

            # One record per line separat | character
            for line in lines:
                date = line.strip().split("|")

                # Reade only the line if it has all 7 fields
                if len(date) == 7:
                    ewaste_records.append({
                        "item_id": date[0],
                        "device_name": date[1],
                        "category": date[2],
                        "weight_kg": float(date[3]),
                        "fee_per_kg": float(date[4]),
                        "status": date[5],
                        "data_added": date[6]
                    })

        print(f"\n Welcome back {len(ewaste_records)} record(s) loaded successfully.")

    except Exception:
        print(f"\n Could not read the saved file. Starting with an empty system.")
        ewaste_records = []

def save_data():
    """Save all current records to the text file so noting is lost on exit."""

    try:
        with open(DATA_FILE, "w") as file:
            # Write each record as one line
            for item in ewaste_records:
                line = (
                    f"{item['item_id']}|"
                    f"{item['device_name']}|"
                    f"{item['category']}|"
                    f"{item['weight_kg']}|"
                    f"{item['fee_per_kg']}|"
                    f"{item['status']}|"
                    f"{item['data_added']}\n"
                )
                file.write(line)

        print("\n All records ware saved successfully.")

    except Exception:
        print("\n  Sorry, something went wrong while saving the date.")

# Display Functions

def display_header(title):
    """Print a section header with titel"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def display_all_items():
    """Show all saved e_waste records in table."""

    display_header("CURRENT E-WASTE RECORDS")

    if not ewaste_records:
        print(" There are currently no record in the system.")
        return

    # Fixed line:
    print(f"{'ID':<8} {'Device':<18} {'Category':<18} {'Weight':<10} {'Status'}")

    for item in ewaste_records:
        print(
            f" {item['item_id']:<8} "
            f"{item['device_name']:<18} "
            f"{item['category']:<18} "
            f"{item['weight_kg']:<10.2f} "
            f"{item['status']}"
        )

    print(f"\n Total Records available: {len(ewaste_records)}")
    show_storage_status()

def show_storage_status():
    """Show how much storage space has been used and give a quick health check."""
    total_weight = sum(item['weight_kg'] for item in ewaste_records)
    percentage = (total_weight / STORAGE_LIMIT_KG) * 100

    print(f"\n  Storage usage: {total_weight:2f}kg / {STORAGE_LIMIT_KG:.0f}kg")
    print(f" Capacity used: {percentage:.1f}%")

    # Inform the user if thing are getting tight
    if percentage >= 100:
        print(" Storage is completely full. ")
    elif percentage >= 80:
        print(" Warning: Storage capacity is getting high. ")
    else:
        print(" Storage levels are safe. ")

    # Helper Funtions

def generate_item_id():
    """Create the next item ID by adding 1 to last item."""
    if not ewaste_records:
        return "EW001"
    
    last_id = ewaste_records[-1]['item_id']
    number = int(last_id[2:]) + 1

    return f"EW{number:03d}"

def find_item(item_id):
    """Search for an item by its ID and return it ornone if not found."""
    for item in ewaste_records:
        if item['item_id'].upper() == item_id.upper():
            return item
    return None

def current_storage_weight():
        """Add the weight of everything in storage"""
        return sum(item['weight_kg'] for item in ewaste_records)

# Add New Item

def add_item():
    """Add a new e-waste item."""

    display_header("REGISTER NEW E-WASTE ITEM")

    if current_storage_weight() >= STORAGE_LIMIT_KG:
        print(" Sorry, storage is already full.")
        return
    
    device_name = input("  Enter device name: ").strip()

    if not device_name:
        print("  Device name can not be empty.")
        return

    # Let the user choose from 3 category options
    print("\n Setct a category")
    print(" 1. Recyclable")
    print(" 2. Hazardous")
    print(" 3. Non-Recyclable")

    choice = input(" Enter your choice: ").strip()

    categories = {
        "1": "Recyclable",
        "2": "Hazardous",
        "3": "Non-Recyclable"
    }

    if choice not in categories:
        print(" Inavlid category selected.")
        return
    
    category = categories[choice]

    # Get and validate the weight
    try:
        weight = float(input(" Enter item weight (kg): "))

        if weight <=0:
            print(" Weight must greater than 0.")
            return
        
    except ValueError:
        print(" Please enter a valid number.")
        return
    
    if current_storage_weight() + weight > STORAGE_LIMIT_KG:
        print(" Not enough storage space for this item.")
        return
    
    # Get and validate the recycling fee
    try:
        fee = float(input(" Enter recycling fee per kg: "))

        if fee < 0:
            print( " Fee cannot be negative.")
            return
        
    except ValueError:
        print(" Please enter a valid fee amount.")
        return
    
    # Create a new record and it to the list
    new_item = {
        "item_id": generate_item_id(),
        "device_name": device_name,
        "category": category,
        "weight_kg": round(weight, 2),
        "fee_per_kg": round(fee, 2),
        "status": "In Storage",
        "data_added": datetime.now().strftime("%Y-%m-%d")
    }

    ewaste_records.append(new_item)

    print(f"\n Item{new_item['item_id']} was added succeefully.")
    print(" The new record has ben saved in the system.")

# Search Items

def search_items():
    """Search for records by item ID or device name."""
    display_header("SEARCH RECORDS")

    if not ewaste_records:
        print(" No records are available now.")
        return
    
    keyword = input(" Enter Item ID or device name: ").lower().strip()

    if not keyword:
        print(" Please enter something for search.")
        return
    
    # Check each record and collext any that match the keyword
    results = []

    for item in ewaste_records:
        if keyword in item['item_id'].lower() or keyword in item['device_name'].lower():
            results.append(item)
        
    if not results:
        print(" No matching record found.")
        return
    
    print(f"\n  {len(results)} matching record(s) found:\n")

    for item in results:
        print(f"  {item['item_id']} - {item['device_name']} ({item['category']})")

# Update Item Status

def update_status():
    """Change status of an exising item."""
    display_header("UPDATE ITEM STATUS")

    if not ewaste_records:
        print(" No records availabale")
        return
    
    item_id = input(" Enter Item ID").strip().upper()

    item = find_item(item_id)

    if item is None:
        print("  Item not fount.")
        return
    
    # Display the avilabale status options
    print("\n  1. Recycled")
    print("  2. Disposed")
    print("  3. In Storage")

    choice = input("  Select new status: ").strip()

    statuses = {
        "1": "Recycled",
        "2": "Disposed",
        "3": "In Storage",
    }

    if choice not in statuses:
        print("  Invalid choice.")
        return
    
    # Apply the new status to the item
    item['status'] = statuses[choice]

    print(f"\n  status updated successfully for {item_id}.")

# Remove Item

def remove_item():
    display_header("REMOVE RECORD")

    if not ewaste_records:
        print("  No records found.")
        return
    
    item_id = input("  Enter Item for remove: ").strip().upper()

    item = find_item(item_id)

    if item is None:
        print("  Item not found.")
        return
    
    # Always confirm befor deleting anything
    confirm = input(f"  Are you sure you want remove {item_id}? (yes/no): ").lower()

    if confirm == "yes":
        ewaste_records.remove(item)
        print("  Record removed susccessfully.")
    else:
        print("  Removal cancelled.")

# Billing

def calculate_fee():
    """Calculate the total recycling payment for one or more items."""
    display_header("CALCULATE RECYCING PAYMENT")

    if not ewaste_records:
        print("  No records available.")
        return
    
    ids = input("  Enter Item IDs separates by commas: ").upper().split(",")

    selected_items = []

    for item_id in ids:
        item = find_item(item_id.strip())

        if item:
            selected_items.append(item)

    if not selected_items:
        print("  No valid item selected.")
        return
    
    total_weight = 0
    subtotal = 0

    print("\n PAYMENT SUMMARY")
    print("  " + "-" * 45)

    # Print the cost for each item and keep a runnig total
    for item in selected_items:
        amount = item['weight_kg'] * item['fee_per_kg']

        total_weight += item['weight_kg']
        subtotal += amount

        print(
            f"  {item['device_name']} - "
            f"{item['weight_kg']}kg = LKR {amount:.2f}"
        )

    discount = 0

    if total_weight > BULK_DISCOUNT_LIMIT:
        discount = subtotal * BULK_DISCOUNT_RATE
        print(f"\n Bulk discount applied: LKR {discount:.2f}")

    final_total = subtotal - discount

    print(f"\n Total Amount: LKR {final_total:.2f}")

# Storage Check

def check_storage():
    """Display a quick overview of how much storage space is left."""

    display_header("STORAGE OVERIEW")

    total = current_storage_weight()
    percentage = (total / STORAGE_LIMIT_KG) * 100

    print(f"  Total weight stored : {total:.2f}kg")
    print(f"  Storage used        : {percentage:.1f}%")
    print(f"  Remaining capacity  : {STORAGE_LIMIT_KG - total:.2F}kg")

    if percentage >= 100:
        print("\n Storage limit reached.")
    elif percentage >= 80:
        print("\n Warning: Storage is almost full.")
    else:
        print("\n Storage levels is good.")

# Alert System



    display_header("ALERTS AND SAFETY CHECKS")

    today = datetime.today()
    found_alert = False

    for item in ewaste_records:

        if item['category'] == "Hazardous" and item['status'] == "In Storage":

            # Work out how many days the item has been stored
            stored_date = datetime.strptime(
                item['data_added'], 
                "%Y-%m-%d"
                )
            
            days = (today - stored_date).days

            if days > HAZARD_LIMIT_DAYS:
                print(
                    f"URGENT: {item['item_id']} "
                    f"({item['device_name']}) " 
                    f"has been stored for {days} days."                
                )
                found_alert = True

        # if no alert were raised only print this massage
        if not found_alert:
            print("  No urgent alerts found today.")

# Report Generation

def generate_report():
    """Write a full summary of all records toa text file."""
    display_header("GENERATE SYSTEM REPORT")

    report_name = (
        f"AEWMS_Report_"
        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    )

    total_weight = sum(item['weight_kg'] for item in ewaste_records)

    with open(report_name, "w") as report:

        report.write("GREEN LANTERN CORPS RECYCLERS\n")
        report.write("Automated E-Waste Management System\n")
        report.write("=" * 50 + "\n\n")

        report.write(f"Generated Date: {datetime.now()}\n")
        report.write(f"Total Records : {len(ewaste_records)}\n")
        report.write(f"Total Weight  : {total_weight:.2f}kg\n\n")

        report.write("ITEM DETAILS\n")
        report.write("-" * 50 + "\n")

        for item in ewaste_records:
            report.write(
                f"{item['item_id']} | "
                f"{item['device_name']} | "
                f"{item['category']} | "
                f"{item['weight_kg']} | "
                f"{item['status']}\n"
            )

    print(f"\n  Report created successfully: {report_name}")

# Menu

def display_menu():
    """Print the main menu so the user can pick what to do."""
    print("\n" + "=" * 60)
    print("  GEEN LANTERN CORPS RECYCLERS")
    print("  Automated E-Waste Management System")
    print("=" * 60)
    print("  1.View all records")
    print("  2.Register new e-waste item")
    print("  3.Search records")
    print("  4.Update item status")
    print("  5.Remove a record")
    print("  6.Calculate recycling payment")
    print("  7.View storage usage")
    print("  8.View alerts and warnings")
    print("  9.Generate system report")
    print("  0.Exit")
    print("=" * 60)

# Main Program

def main():
    """Start the prongram then load saved data and keep the menu runnig."""

    print("\n  Starting AEWMS System...")

    load_data()

    actions = {
        "1": display_all_items,
        "2": add_item,
        "3": search_items,
        "4": update_status,
        "5": remove_item,
        "6": calculate_fee,
        "7": check_storage,
        "8": search_items,
        "9": generate_report,           
    }

    while True:

        display_menu()

        choice = input("\n Select an option: ").strip()

        if choice == "0":
            # SAVE EVERYTHING BEFOR CLOSING
            save_data()
            print("\n  Thank you for using AEWMS system.")
            print("  Have a great day!")
            break
        
        elif choice in actions:
            actions[choice]()
            input("\n  Press Enter to return to menu...")

        else:
            print("\n  please try again.")

if __name__ == "__main__":
    main()