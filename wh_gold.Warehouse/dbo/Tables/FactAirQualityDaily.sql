CREATE TABLE [dbo].[FactAirQualityDaily] (
    [date_key]    DATE           NULL,
    [location_id] BIGINT         NULL,
    [sensor_id]   BIGINT         NULL,
    [parameter]   VARCHAR (8000) NULL,
    [value]       FLOAT (53)     NULL,
    [units]       VARCHAR (8000) NULL
);


GO