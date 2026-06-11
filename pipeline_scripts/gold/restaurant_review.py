from pyspark.sql.functions import *
from pyspark import pipelines as dp

@dp.materialized_view(
    name="restaurant_review",
    table_properties={"quality": "gold"}
)
def restaurant_review() :

    df_reviews = (
        spark.read.table("resturant.silver.fact_reviews")
        .groupBy(col("restaurant_id"))
        .agg(
            count(col("review_id")).alias("total_reviews"),
            avg(col("rating")).cast("decimal(3,2)").alias("avg_rating"),
            sum(when(col("rating") == 5, 1).otherwise(0)).alias("rating_5_count"),
            sum(when(col("rating") == 4, 1).otherwise(0)).alias("rating_4_count"),
            sum(when(col("rating") == 3, 1).otherwise(0)).alias("rating_3_count"),
            sum(when(col("rating") == 2, 1).otherwise(0)).alias("rating_2_count"),
            sum(when(col("rating") == 1, 1).otherwise(0)).alias("rating_1_count"),
            sum(when(col("sentiment") == "positive", 1).otherwise(0)).alias("sentiment_positive_count"),
            sum(when(col("sentiment") == "neutral", 1).otherwise(0)).alias("sentiment_neutral_count"),
            sum(when(col("sentiment") == "negative", 1).otherwise(0)).alias("sentiment_negative_count")
        )
    )

    df_restaurant = spark.read.table("resturant.silver.dim_resturants")

    df = (
        df_restaurant.join(df_reviews, on="restaurant_id", how="left")
        .select(
            col("restaurant_id"),
            col("name").alias("restaurant_name"),
            col("city").alias("restaurant_city"),
            coalesce(col("total_reviews"), lit(0)).alias("total_reviews"),
            coalesce(col("avg_rating"), lit(0)).cast("decimal(3,2)").alias("avg_rating"),
            coalesce(col("rating_5_count"), lit(0)).alias("rating_5_count"),
            coalesce(col("rating_4_count"), lit(0)).alias("rating_4_count"),
            coalesce(col("rating_3_count"), lit(0)).alias("rating_3_count"),
            coalesce(col("rating_2_count"), lit(0)).alias("rating_2_count"),
            coalesce(col("rating_1_count"), lit(0)).alias("rating_1_count"),
            coalesce(col("sentiment_positive_count"), lit(0)).alias("sentiment_positive_count"),
            coalesce(col("sentiment_neutral_count"), lit(0)).alias("sentiment_neutral_count"),
            coalesce(col("sentiment_negative_count"), lit(0)).alias("sentiment_negative_count")
        )
    )

    return df