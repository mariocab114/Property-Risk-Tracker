from database import create_table, add_property, delete_property, get_all_properties, update_property
from models import Property

def get_valid_risk_score():
    while True:
        score = input("Risk score (1-10): ")
        try:
            score = int(score)
            if 1 <= score <= 10:
                return score
            else:
                print("Risk score must be between 1 and 10. Try again.")
        except ValueError:
            print("Please enter a whole number.")

def get_valid_risk_category():
    valid_categories = ["Fire", "Flood", "Equipment", "Wind", "Theft"]
    while True:
        category = input(f"Risk category ({', '.join(valid_categories)}): ")
        if category.title() in valid_categories:
            return category.title()
        else:
            print(f"Please choose one of: {', '.join(valid_categories)}")

def add_new_property():
    print("\n--- Add a New Property ---")
    name = input("Property name: ")
    location = input("Location: ")
    value = get_valid_value()
    risk_category = get_valid_risk_category()
    risk_score = get_valid_risk_score()
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

#MENU
def main():
    create_table()
    while True:
        print("\n=== Property Risk Tracker ===")
        print("1. Add a property")
        print("2. View all properties")
        print("3. Delete a property")
        print("4. Analyze risk")
        print("5. Export to CSV")
        print("6. Import from CSV")
        print("7. Update a property")
        print("8. AI risk segmentation")
        print("9. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            add_new_property()
        elif choice == "2":
            view_all_properties()
        elif choice == "3":
            delete_property_by_id()
        elif choice == "4":
            analyze_risk()
        elif choice == "5":
            export_to_csv()
        elif choice == "6":
            import_from_csv()
        elif choice == "7":
            update_property_by_id()
        elif choice == "8":
            ai_risk_segmentation()
        elif choice == "9":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")

def delete_property_by_id():
    view_all_properties()
    property_id = int(input("\nEnter the ID of the property to delete: "))
    delete_property(property_id)
    print("✓ Property deleted.")

def get_valid_value():
    while True:
        value_input = input("Value ($): ").replace(",", "")
        try:
            return float(value_input)
        except ValueError:
            print("Please enter a valid number (e.g. 450000 or 450000.50).")

import pandas as pd

def analyze_risk():
    print("\n--- Risk Analysis ---")
    rows = get_all_properties()
    if not rows:
        print("No properties yet.")
        return

    df = pd.DataFrame(rows, columns=["id", "name", "location", "value", "risk_category", "risk_score"])

    df["risk_exposure"] = df["value"] * (df["risk_score"] / 10)

    print("\nAll properties, ranked by risk exposure (value x risk score):")
    ranked = df.sort_values("risk_exposure", ascending=False)
    for _, row in ranked.iterrows():
        print(f"{row['name']} ({row['location']}) - Exposure: ${row['risk_exposure']:,.2f}")

    print(f"\nTotal portfolio value: ${df['value'].sum():,.2f}")
    print(f"Average risk score: {df['risk_score'].mean():.1f}/10")
    print(f"Highest exposure property: {ranked.iloc[0]['name']}")

def export_to_csv():
    print("\n--- Export to CSV ---")
    rows = get_all_properties()
    if not rows:
        print("No properties yet.")
        return

    df = pd.DataFrame(rows, columns=["id", "name", "location", "value", "risk_category", "risk_score"])
    filename = input("Enter filename to save as (e.g. properties.csv): ")
    df.to_csv(filename, index=False)
    print(f"✓ Exported {len(df)} properties to {filename}")

def import_from_csv():
    print("\n--- Import from CSV ---")
    filename = input("Enter filename to import (e.g. properties.csv): ")
    try:
        df = pd.read_csv(filename)
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return

    count = 0
    for _, row in df.iterrows():
        new_property = Property(row["name"], row["location"], row["value"], row["risk_category"], row["risk_score"])
        add_property(new_property)
        count += 1
    print(f"✓ Imported {count} properties from {filename}")

def update_property_by_id():
    view_all_properties()
    property_id = int(input("\nEnter the ID of the property to update: "))

    rows = get_all_properties()
    current = None
    for row in rows:
        if row[0] == property_id:
            current = row
            break

    if not current:
        print("No property found with that ID.")
        return

    print("Enter new values (leave blank to keep current value):")
    name = input(f"Name [{current[1]}]: ") or current[1]
    location = input(f"Location [{current[2]}]: ") or current[2]
    print(f"Current value: {current[3]}")
    change_value = input("Change value?: ")
    value = get_valid_value() if change_value.lower() == "y" else current[3]
    print(f"Current risk category: {current[4]}")

    change_category = input("Change risk category?: ")
    risk_category = get_valid_risk_category() if change_category.lower() == "y" else current[4]

    print(f"Current risk score: {current[5]}")
    change_score = input("Change risk score?: ")
    risk_score = get_valid_risk_score() if change_score.lower() == "y" else current[5]

    update_property(property_id, name, location, value, risk_category, risk_score)
    print("✓ Property updated.")
    
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def ai_risk_segmentation():
    print("\n--- AI Risk Segmentation ---")
    rows = get_all_properties()
    if len(rows) < 3:
        print("Need at least 3 properties for this feature to work well.")
        return

    df = pd.DataFrame(rows, columns=["id", "name", "location", "value", "risk_category", "risk_score"])

    features = df[["value", "risk_score"]]
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    df["cluster"] = kmeans.fit_predict(scaled_features)

    cluster_avg_risk = df.groupby("cluster")["risk_score"].mean().sort_values()
    tier_names = {}
    tier_labels = ["Low Risk Tier", "Medium Risk Tier", "High Risk Tier"]
    for tier_name, cluster_id in zip(tier_labels, cluster_avg_risk.index):
        tier_names[cluster_id] = tier_name

    df["risk_tier"] = df["cluster"].map(tier_names)

    for tier in tier_labels:
        print(f"\n{tier}:")
        matches = df[df["risk_tier"] == tier]
        for _, row in matches.iterrows():
            print(f"  {row['name']} - Value: ${row['value']:,.2f}, Risk Score: {row['risk_score']}/10")

if __name__ == "__main__":
    main()

