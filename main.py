import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from database import (
    add_property,
    create_table,
    delete_property,
    get_all_properties,
    get_exposure_ranking,
    get_risk_categories,
    update_property,
)
from models import Property


# ---------- Input validation ----------

def get_valid_id(prompt):
    while True:
        entry = input(prompt).strip()
        if entry.isdigit():
            return int(entry)
        print("Please enter a numeric ID (for example, 3).")


def get_valid_value():
    while True:
        value_input = input("Value ($): ").replace(",", "")
        try:
            return float(value_input)
        except ValueError:
            print("Please enter a valid number (e.g. 450000 or 450000.50).")


def get_valid_risk_score():
    while True:
        score = input("Risk score (1-10): ")
        try:
            score = int(score)
            if 1 <= score <= 10:
                return score
            print("Risk score must be between 1 and 10. Try again.")
        except ValueError:
            print("Please enter a whole number.")


def get_valid_risk_category():
    categories = get_risk_categories()
    while True:
        entry = input(f"Risk category ({', '.join(categories)}): ").strip()
        for category in categories:
            if entry.lower() == category.lower():
                return category
        print(f"Please choose one of: {', '.join(categories)}")


def property_exists(property_id):
    return property_id in [row[0] for row in get_all_properties()]


# ---------- Menu actions ----------

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


def delete_property_by_id():
    view_all_properties()
    property_id = get_valid_id("\nEnter the ID of the property to delete: ")
    if not property_exists(property_id):
        print("No property found with that ID.")
        return
    delete_property(property_id)
    print("✓ Property deleted.")


def analyze_risk():
    print("\n--- Risk Analysis ---")
    categories = get_risk_categories()
    entry = input(f"Filter by category ({', '.join(categories)}) or press Enter for all: ").strip()
    selected = next((c for c in categories if c.lower() == entry.lower()), None)
    if entry and selected is None:
        print("Unknown category, showing all properties.")

    ranking = get_exposure_ranking(selected)
    if not ranking:
        print("No properties found.")
        return

    print("\nRanked by risk exposure (value x risk score), calculated in SQL Server:")
    for rank, name, location, category, value, score, exposure in ranking:
        print(f"{rank}. {name} ({location}) - {category} - Exposure: {exposure:,.0f}")

    total_value = sum(r[4] for r in ranking)
    avg_score = sum(r[5] for r in ranking) / len(ranking)
    print(f"\nTotal portfolio value: ${total_value:,.2f}")
    print(f"Average risk score: {avg_score:.1f}/10")
    print(f"Highest exposure property: {ranking[0][1]}")


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
        new_property = Property(
            str(row["name"]),
            str(row["location"]),
            float(row["value"]),
            str(row["risk_category"]),
            int(row["risk_score"]),
        )
        add_property(new_property)
        count += 1
    print(f"✓ Imported {count} properties from {filename}")


def update_property_by_id():
    view_all_properties()
    property_id = get_valid_id("\nEnter the ID of the property to update: ")

    current = next((row for row in get_all_properties() if row[0] == property_id), None)
    if not current:
        print("No property found with that ID.")
        return

    print("Enter new values (leave blank to keep current value):")
    name = input(f"Name [{current[1]}]: ") or current[1]
    location = input(f"Location [{current[2]}]: ") or current[2]

    print(f"Current value: {current[3]}")
    value = get_valid_value() if input("Change value? (y/n): ").lower() == "y" else current[3]

    print(f"Current risk category: {current[4]}")
    risk_category = get_valid_risk_category() if input("Change risk category? (y/n): ").lower() == "y" else current[4]

    print(f"Current risk score: {current[5]}")
    risk_score = get_valid_risk_score() if input("Change risk score? (y/n): ").lower() == "y" else current[5]

    update_property(property_id, name, location, value, risk_category, risk_score)
    print("✓ Property updated.")


def ai_risk_segmentation():
    print("\n--- AI Risk Segmentation ---")
    rows = get_all_properties()
    if len(rows) < 3:
        print("Need at least 3 properties for this feature to work well.")
        return

    df = pd.DataFrame(rows, columns=["id", "name", "location", "value", "risk_category", "risk_score"])

    scaled_features = StandardScaler().fit_transform(df[["value", "risk_score"]])
    df["cluster"] = KMeans(n_clusters=3, random_state=42, n_init=10).fit_predict(scaled_features)

    tier_labels = ["Low Risk Tier", "Medium Risk Tier", "High Risk Tier"]
    cluster_order = df.groupby("cluster")["risk_score"].mean().sort_values().index
    df["risk_tier"] = df["cluster"].map(dict(zip(cluster_order, tier_labels)))

    for tier in tier_labels:
        print(f"\n{tier}:")
        for _, row in df[df["risk_tier"] == tier].iterrows():
            print(f"  {row['name']} - Value: ${row['value']:,.2f}, Risk Score: {row['risk_score']}/10")


# ---------- Menu ----------

def main():
    create_table()
    actions = {
        "1": add_new_property,
        "2": view_all_properties,
        "3": delete_property_by_id,
        "4": analyze_risk,
        "5": export_to_csv,
        "6": import_from_csv,
        "7": update_property_by_id,
        "8": ai_risk_segmentation,
    }
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
        choice = input("Choose an option: ").strip()

        if choice == "9":
            print("Goodbye!")
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()