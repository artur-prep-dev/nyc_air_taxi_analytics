create   PROCEDURE dbo.load_star_schema 
as 
begin
    drop table if exists dbo.DimZone;
    create table dbo.DimZone As
    select 
        LocationID as zone_id,
        Borough as borough,
        Zone as zone_name,
        service_zone
    From lh_silver.dbo.taxi_zones;

    drop table if exists dbo.DimGDP;
    create table dbo.DimGDP as 
    select 
        year,
        country_id,
        country_name,
        gdp_usd
    from lh_silver.dbo.gdp_usa;

    drop table if exists dbo.DimDate
    create table dbo.DimDate as 
    select DISTINCT
        pickup_date as date_key,
        year(pickup_date) as year,
        month(pickup_date) as month,
        day(pickup_date) as day,
        datepart(weekday, pickup_date) as weekday_number 
    from lh_gold.dbo.fact_taxi_daily;

    drop table if exists dbo.DimFX;
    create table dbo.DimFX as 
    select 
        d.date_key,
        (select top 1 f.usd_per_eur
        from lh_silver.dbo.fx_usd_eur as f
        where f.date <=d.date_key
        order by f.date desc) as usd_per_eur 
    from dbo.DimDate as d;

    drop table if exists dbo.FactTaxiDaily;
    create table dbo.FactTaxiDaily as 
    select 
        pickup_date as date_key,
        PULocationID as zone_id,
        trips_count,
        revenue as revenue_usd,
        avg_distance 
    from lh_gold.dbo.fact_taxi_daily;

    drop table if exists dbo.FactAirQualityDaily;
    create table dbo.FactAirQualityDaily as 
    select 
        date as date_key,
        location_id,
        sensor_id,
        parameter,
        value,
        units
    from lh_silver.dbo.air_quality_daily;

END;

GO