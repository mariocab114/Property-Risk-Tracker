USE PropertyRiskTracker;
GO

CREATE TABLE risk_categories (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE properties (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(100) NOT NULL,
    location NVARCHAR(100) NOT NULL,
    risk_category_id INT NOT NULL
        FOREIGN KEY REFERENCES risk_categories(id)
);

CREATE TABLE valuations (
    id INT IDENTITY(1,1) PRIMARY KEY,
    property_id INT NOT NULL
        FOREIGN KEY REFERENCES properties(id),
    value DECIMAL(15,2) NOT NULL,
    risk_score INT NOT NULL
);