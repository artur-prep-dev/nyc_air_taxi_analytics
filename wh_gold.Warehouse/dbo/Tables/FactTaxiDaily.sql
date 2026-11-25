CREATE TABLE [dbo].[FactTaxiDaily] (
    [date_key]     DATE       NULL,
    [zone_id]      INT        NULL,
    [trips_count]  BIGINT     NULL,
    [revenue_usd]  FLOAT (53) NULL,
    [avg_distance] FLOAT (53) NULL
);


GO