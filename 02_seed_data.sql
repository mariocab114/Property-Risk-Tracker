USE PropertyRiskTracker;
GO

INSERT INTO risk_categories (name)
VALUES ('Fire'), ('Flood'), ('Earthquake'), ('Windstorm'), ('Theft');

INSERT INTO properties (name, location, risk_category_id)
VALUES
    ('Warehouse A', 'Chicago', 1),
    ('Office B', 'Boston', 2),
    ('Plant C', 'San Francisco', 3),
    ('Store D', 'Miami', 4),
    ('Depot E', 'Houston', 2);

INSERT INTO valuations (property_id, value, risk_score)
VALUES
    (1, 450000, 7),
    (2, 200000, 5),
    (3, 1200000, 9),
    (4, 350000, 6),
    (5, 800000, 8);