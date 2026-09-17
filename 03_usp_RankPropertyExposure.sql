USE PropertyRiskTracker;
GO

CREATE OR ALTER PROCEDURE dbo.usp_RankPropertyExposure
    @RiskCategory NVARCHAR(50) = NULL
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        RANK() OVER (ORDER BY v.value * v.risk_score DESC) AS exposure_rank,
        p.name,
        p.location,
        r.name AS risk_category,
        v.value,
        v.risk_score,
        v.value * v.risk_score AS exposure
    FROM properties p
    JOIN risk_categories r ON p.risk_category_id = r.id
    JOIN valuations v ON v.property_id = p.id
    WHERE @RiskCategory IS NULL OR r.name = @RiskCategory
    ORDER BY exposure DESC;
END;