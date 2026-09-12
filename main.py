from database import create_table, add_property, delete_property, get_all_properties, delete_property 
from models import Property
def add_new_property():
    print("\n--- Add a New Property ---")
    name = input("Property name: ")
    location = input("Location: ")
    value = float(input("Value ($): ").replace(",", ""))
    risk_category = input("Risk category (e.g. Fire, Flood, Equipment): ")
    risk_score = int(input("Risk score (1-10): "))
    new_property = Property(name, location, value, risk_category, risk_score)
    add_property(new_property)
    print(f"\n✓ Added: {new_property}")

def view_all_properties():
    print("\n--- All Properties ---")
    rows = get_all_properties()
    if not rows:
        print("No properties yet.")
        return
    for row in rows:
        print(f"ID {row[0]}: {row[1]} ({row[2]}) - Value: ${row[3]:,.2f}, Risk: {row[4]} ({row[5]}/10)")
1
def main():
    create_table()
    while True:
        print("\n=== Property Risk Tracker ===")
        print("1. Add a property")
        print("2. View all properties")
        print("3. Delete a property")
        print("4. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            add_new_property()
        elif choice == "2":
            view_all_properties()
        elif choice == "3":
            delete_property_by_id()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")
def delete_property_by_id():
    view_all_properties()
    property_id = int(input("\nEnter the ID of the property to delete: "))
    delete_property(property_id)
    print("✓ Property deleted.")
if __name__ == "__main__":
    main()