from pyspark.sql.functions import *
from pyspark.sql.window import Window
from pyspark import pipelines as dp

@dp.materialized_view(
    name="cust_360",
    table_properties={"quality": "gold"}
)
def cust_360() :
    df_customers = spark.read.table("resturant.silver.dim_customers")
    df_orders = spark.read.table("resturant.silver.fact_orders")
    df_order_items = spark.read.table("resturant.silver.fact_order_items")
    df_restaurant = spark.read.table("resturant.silver.dim_resturants")
    df_reviews = spark.read.table("resturant.silver.fact_reviews")

    df_order_stats = (
        df_orders
        .groupBy(col("customer_id"))
        .agg(
            countDistinct(col("order_id")).alias("total_orders"),
            sum(col("total_amount")).cast("decimal(10,2)").alias("lifetime_spend"),
            avg(col("total_amount")).cast("decimal(10,2)").alias("avg_order_value"),
            max(col("order_date")).alias("last_order_date")
        )
        .withColumn("loyalty_tier",
                    when(col("lifetime_spend") >= 25000, "Platinum")
                    .when(col("lifetime_spend") >= 15000, "Gold")
                    .when(col("lifetime_spend") >= 5000, "Silver")
                    .otherwise("Bronze")
        )
    )

    df_reviews_stats = (
        df_reviews
        .groupBy(col("customer_id"))
        .agg(
            avg(col("rating")).cast("decimal(3,2)").alias("avg_rating_given"),
            count(col("review_id")).alias("total_reviews")
        )
    )

    df_fav_restaurant = (
        df_orders
        .groupBy(col("customer_id"), col("restaurant_id"))
        .agg(
            count(col("order_id")).alias("total_order_cnt")
        )
        .withColumn("rn", row_number().over(Window.partitionBy(col("customer_id")).orderBy(col("total_order_cnt").desc())))
        .filter(col("rn") == 1)
        .join(df_restaurant, on="restaurant_id", how="left")
        .select(
            col("customer_id"),
            col("name").alias("favorite_restaurant")
        )
    )

    df_fav_item = (
        df_order_items.join(df_orders, on="order_id", how="inner")
        .groupBy(col("customer_id"), col("item_name"))
        .agg(
            sum(col("quantity")).alias("total_item_quantity")
        )
        .withColumn("rn", row_number().over(Window.partitionBy(col("customer_id")).orderBy(col("total_item_quantity").desc())))
        .filter(col("rn") == 1)
        .select(
            col("customer_id"),
            col("item_name").alias("favorite_item")
        )
    )

    df_cust_360 = (
        df_customers.join(df_order_stats, on="customer_id", how="left")
        .join(df_reviews_stats, on="customer_id", how="left")
        .join(df_fav_restaurant, on="customer_id", how="left")
        .join(df_fav_item, on="customer_id", how="left")
        .select(
            col("customer_id"),
            col("name"),
            col("email"),
            col("city"),
            col("join_date"),
            
            coalesce(col("total_orders"), lit(0)).alias("total_orders"),
            coalesce(col("lifetime_spend"), lit(0)).cast("decimal(10,2)").alias("lifetime_spend"),
            coalesce(col("avg_order_value"), lit(0)).cast("decimal(10,2)").alias("avg_order_value"),
            col("last_order_date"),
            coalesce(col("loyalty_tier"), lit("Bronze")).alias("loyalty_tier"),
            
            coalesce(col("avg_rating_given"), lit(0)).cast("decimal(3,2)").alias("avg_rating_given"),
            coalesce(col("total_reviews"), lit(0)).alias("total_reviews"),

            col("favorite_restaurant"),
            col("favorite_item")
        )
    )

    return df_cust_360


