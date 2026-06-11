CREATE OR REFRESH STREAMING TABLE resturant.silver.fact_reviews (
    CONSTRAINT valid_review_id EXPECT (review_id IS NOT NULL) ON VIOLATION DROP ROW,
    CONSTRAINT valid_rating EXPECT (rating > 0) ON VIOLATION DROP ROW,
    CONSTRAINT valid_sentiment EXPECT (sentiment IN ('positive', 'neutral', 'negative')) ON VIOLATION DROP ROW
)
TBLPROPERTIES (
    "quality" = 'silver'
)
AS
SELECT
    review_id,
    order_id,
    customer_id,
    restaurant_id,
    rating,
    review_text,
    response_json,
    response_json:sentiment as sentiment,
    response_json:issue_delivery::boolean as issue_delivery,
    response_json:issue_delivery_reason as issue_delivery_reason,
    response_json:issue_food_quality::boolean as issue_food_quality,
    response_json:issue_food_quality_reason as issue_food_quality_reason,
    response_json:issue_pricing::boolean as issue_pricing,
    response_json:issue_pricing_reason as issue_pricing_reason,
    response_json:issue_portion_size::boolean as issue_portion_size,
    response_json:issue_portion_size_reason as issue_portion_size_reason,
    review_timestamp
FROM (
    SELECT 
        *,
        ai_query(
            "databricks-gpt-oss-20b",
            CONCAT(
                'Analyze the following review and return ONLY a valid JSON object with this exact structure: ',
                '{"sentiment": "<positive/neutral/negative>", ',
                '"issue_delivery": <true/false>, ',
                '"issue_delivery_reason": "<reason or empty string>", ',
                '"issue_food_quality": <true/false>, ',
                '"issue_food_quality_reason": "<reason or empty string>", ',
                '"issue_pricing": <true/false>, ',
                '"issue_pricing_reason": "<reason or empty string>", ',
                '"issue_portion_size": <true/false>, ',
                '"issue_portion_size_reason": "<reason or empty string>"}. ',
                'Rules: sentiment must be exactly one of: positive, neutral, negative. ',
                'Each issue field is true/false only. ',
                'Each reason field should contain a brief explanation if the issue is true, otherwise empty string. ',
                'Review text: ', review_text)
        ) AS response_json
    FROM STREAM(resturant.bronze.reviews)
);