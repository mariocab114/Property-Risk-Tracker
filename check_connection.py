import pyodbc

CONNECTION_STRING = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=PropertyRiskTracker;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

with pyodbc.connect(CONNECTION_STRING) as conn:
    cursor = conn.cursor()
    cursor.execute("EXEC dbo.usp_RankPropertyExposure @RiskCategory = ?", "Flood")
    for row in cursor.fetchall():
        print(row.exposure_rank, row.name, row.location, row.exposure)