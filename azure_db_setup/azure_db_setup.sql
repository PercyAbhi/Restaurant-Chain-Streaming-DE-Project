CREATE SCHEMA birbal_darbar;
GO

CREATE TABLE  birbal_darbar.historical_orders (
    order_id VARCHAR(256) PRIMARY KEY,
    order_timestamp DATETIME2,
    restaurant_id VARCHAR(256),
    customer_id VARCHAR(256),
    order_type VARCHAR(256),
    items VARCHAR(MAX),
    total_amount DECIMAL,
    payment_method VARCHAR(256),
    order_status VARCHAR(256)
);

CREATE TABLE birbal_darbar.reviews (
    review_id VARCHAR(256) PRIMARY KEY,
    order_id VARCHAR(256),
    customer_id VARCHAR(256),
    restaurant_id VARCHAR(256),
    review_text VARCHAR(MAX),
    rating INT,
    review_timestamp DATETIME2
);

CREATE TABLE birbal_darbar.customers (
    customer_id VARCHAR(256) PRIMARY KEY,
    name VARCHAR(256),
    email VARCHAR(256),
    phone VARCHAR(256),
    city VARCHAR(256),
    join_date DATE,
);

CREATE TABLE birbal_darbar.menu_items (
    restaurant_id VARCHAR(256),
    item_id VARCHAR(256),
    name VARCHAR(256),
    category VARCHAR(256),
    price DECIMAL(10,2),
    ingredients VARCHAR(256),
    is_vegetarian BIT,
    spice_level VARCHAR(256),
    PRIMARY KEY (restaurant_id, item_id)
);

CREATE TABLE birbal_darbar.restaurants (
    restaurant_id VARCHAR(256) PRIMARY KEY,
    name VARCHAR(256),
    city VARCHAR(256),
    country VARCHAR(256),
    address VARCHAR(MAX),
    opening_date DATE,
    phone VARCHAR(256)
);
GO

ALTER DATABASE resturantsDB SET CHANGE_TRACKING = ON (CHANGE_RETENTION = 14 DAYS, AUTO_CLEANUP = ON);

ALTER TABLE birbal_darbar.customers ENABLE CHANGE_TRACKING;
ALTER TABLE birbal_darbar.historical_orders ENABLE CHANGE_TRACKING;
ALTER TABLE birbal_darbar.menu_items ENABLE CHANGE_TRACKING;
ALTER TABLE birbal_darbar.restaurants ENABLE CHANGE_TRACKING;
ALTER TABLE birbal_darbar.reviews ENABLE CHANGE_TRACKING;

EXEC sys.sp_cdc_enable_db;

EXEC sys.sp_cdc_enable_table
    @source_schema = N'birbal_darbar',
    @source_name   = N'customers',
    @role_name     = NULL;


EXEC sys.sp_cdc_enable_table
    @source_schema = N'birbal_darbar',
    @source_name   = N'historical_orders',
    @role_name     = NULL;


EXEC sys.sp_cdc_enable_table
    @source_schema = N'birbal_darbar',
    @source_name   = N'menu_items',
    @role_name     = NULL;


EXEC sys.sp_cdc_enable_table
    @source_schema = N'birbal_darbar',
    @source_name   = N'restaurants',
    @role_name     = NULL;


EXEC sys.sp_cdc_enable_table
    @source_schema = N'birbal_darbar',
    @source_name   = N'reviews',
    @role_name     = NULL;


EXEC dbo.lakeflowFixPermissions
    @User = 'admin_sqlserver',
    @Tables = 'ALL';

EXEC dbo.lakeflowSetupChangeTracking
    @Tables = 'ALL',
    @User = 'admin_sqlserver';

EXEC dbo.lakeflowSetupChangeDataCapture
    @Tables = 'ALL',
    @User = 'admin_sqlserver';

-- Validation Queries

SELECT
    d.name AS DatabaseName,
    ctd.is_auto_cleanup_on,
    ctd.retention_period,
    ctd.retention_period_units_desc
FROM sys.change_tracking_databases ctd
INNER JOIN sys.databases d ON ctd.database_id = d.database_id
WHERE d.name = DB_NAME();

SELECT
    SCHEMA_NAME(t.schema_id) + '.' + t.name AS TableName,
    ct.is_track_columns_updated_on,
    ct.begin_version,
    ct.cleanup_version
FROM sys.change_tracking_tables ct
INNER JOIN sys.tables t ON ct.object_id = t.object_id;

SELECT
    SCHEMA_NAME(t.schema_id) + '.' + t.name AS TableName,
    ct.capture_instance,
    ct.start_lsn,
    ct.create_date
FROM cdc.change_tables ct
INNER JOIN sys.tables t ON ct.source_object_id = t.object_id;