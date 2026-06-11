import os
import importlib

from dotenv import load_dotenv
load_dotenv()


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(os.path.join(script_dir, "data"), exist_ok=True)

    seed_data = importlib.import_module("00_seed_restaurant_data")
    seed_data.generate_seed_resturant_data()

    historical_orders = importlib.import_module("01_historical_orders")
    historical_orders.generate_historical_orders(num_orders=10000)

    reviews = importlib.import_module("02_reviews")
    reviews.generate_customer_reviews(review_percentage=0.30)
