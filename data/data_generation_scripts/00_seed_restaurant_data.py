import pandas as pd
import random
import os
from faker import Faker

fake = Faker(['en_IN'])

# ============================================
# RESTAURANTS
# ============================================
def generate_restaurants():
    restaurants_data = [
        {
            "restaurant_id": "REST-DEL-001",
            "name": "Birbal Darbar Connaught Place",
            "city": "Delhi",
            "country": "India",
            "address": "Hanuman Road, Connaught Place",
            "opening_date": "2023-01-15",
            "phone": "+91 973-123-4567"
        },
        {
            "restaurant_id": "REST-DEL-002",
            "name": "Birbal Darbar Chanakyapuri",
            "city": "Delhi",
            "country": "India",
            "address": "The Chanakya Mall, Chanakyapuri",
            "opening_date": "2023-06-20",
            "phone": "+91 973-234-5678"
        },
        {
            "restaurant_id": "REST-MUM-001",
            "name": "Birbal Darbar Bandra",
            "city": "Mumbai",
            "country": "India",
            "address": "Chapel Road, Bandra",
            "opening_date": "2023-03-10",
            "phone": "+91 974-345-6789"
        },
        {
            "restaurant_id": "REST-MUM-002",
            "name": "Birbal Darbar Seawoods",
            "city": "Navi Mumbai",
            "country": "India",
            "address": "Grand Central Mall, Seawoods",
            "opening_date": "2023-09-05",
            "phone": "+91 974-456-7890"
        },
        {
            "restaurant_id": "REST-BLR-001",
            "name": "Birbal Darbar Koramangala",
            "city": "Bengaluru",
            "country": "India",
            "address": "KHB Colony, Koramangala",
            "opening_date": "2024-02-14",
            "phone": "+91 976-567-8901"
        }
    ]

    df_restaurants = pd.DataFrame(restaurants_data)
    return df_restaurants

# ============================================
# MENU ITEMS (Master List)
# ============================================
def generate_menu_items():
    master_menu = [
        # Starters
        {"item_id": "ITEM-101", "name": "Samosa (2 pcs)", "category": "Starter", "price": 120.00, "ingredients": "Potato, Peas, Spices, Pastry", "is_vegetarian": True, "spice_level": "Medium"},
        {"item_id": "ITEM-102", "name": "Paneer Tikka", "category": "Starter", "price": 235.00, "ingredients": "Paneer, Yogurt, Spices, Bell Pepper", "is_vegetarian": True, "spice_level": "Medium"},
        {"item_id": "ITEM-103", "name": "Chicken 65", "category": "Starter", "price": 380.00, "ingredients": "Chicken, Curry Leaves, Spices", "is_vegetarian": False, "spice_level": "Hot"},
        {"item_id": "ITEM-104", "name": "Aloo Tikki Chaat", "category": "Starter", "price": 220.00, "ingredients": "Potato, Chickpeas, Yogurt, Tamarind", "is_vegetarian": True, "spice_level": "Mild"},
        {"item_id": "ITEM-105", "name": "Chicken Seekh Kebab", "category": "Starter", "price": 320.00, "ingredients": "Minced Chicken, Spices, Onion", "is_vegetarian": False, "spice_level": "Medium"},
        
        # Main Course - Vegetarian
        {"item_id": "ITEM-201", "name": "Paneer Butter Masala", "category": "Main Course", "price": 345.00, "ingredients": "Paneer, Tomato, Cream, Butter", "is_vegetarian": True, "spice_level": "Mild"},
        {"item_id": "ITEM-202", "name": "Dal Makhani", "category": "Main Course", "price": 310.00, "ingredients": "Black Lentils, Kidney Beans, Cream", "is_vegetarian": True, "spice_level": "Mild"},
        {"item_id": "ITEM-203", "name": "Palak Paneer", "category": "Main Course", "price": 420.00, "ingredients": "Spinach, Paneer, Spices", "is_vegetarian": True, "spice_level": "Medium"},
        {"item_id": "ITEM-204", "name": "Malai Kofta", "category": "Main Course", "price": 440.00, "ingredients": "Cottage Cheese, Potato, Cashew Gravy", "is_vegetarian": True, "spice_level": "Mild"},
        {"item_id": "ITEM-205", "name": "Chole Bhature", "category": "Main Course", "price": 400.00, "ingredients": "Chickpeas, Fried Bread, Spices", "is_vegetarian": True, "spice_level": "Medium"},
        
        # Main Course - Non-Vegetarian
        {"item_id": "ITEM-301", "name": "Butter Chicken", "category": "Main Course", "price": 520.00, "ingredients": "Chicken, Tomato, Butter, Cream", "is_vegetarian": False, "spice_level": "Mild"},
        {"item_id": "ITEM-302", "name": "Chicken Tikka Masala", "category": "Main Course", "price": 500.00, "ingredients": "Chicken Tikka, Tomato Gravy, Cream", "is_vegetarian": False, "spice_level": "Medium"},
        {"item_id": "ITEM-303", "name": "Lamb Rogan Josh", "category": "Main Course", "price": 650.00, "ingredients": "Lamb, Yogurt, Kashmiri Spices", "is_vegetarian": False, "spice_level": "Medium"},
        {"item_id": "ITEM-304", "name": "Fish Curry", "category": "Main Course", "price": 550.00, "ingredients": "Fish, Coconut, Curry Leaves", "is_vegetarian": False, "spice_level": "Hot"},
        {"item_id": "ITEM-305", "name": "Chicken Biryani", "category": "Main Course", "price": 480.00, "ingredients": "Basmati Rice, Chicken, Saffron, Spices", "is_vegetarian": False, "spice_level": "Medium"},
        
        # Rice & Breads
        {"item_id": "ITEM-401", "name": "Naan", "category": "Bread", "price": 80.00, "ingredients": "Flour, Yogurt, Yeast", "is_vegetarian": True, "spice_level": "None"},
        {"item_id": "ITEM-402", "name": "Garlic Naan", "category": "Bread", "price": 100.00, "ingredients": "Flour, Garlic, Butter", "is_vegetarian": True, "spice_level": "None"},
        {"item_id": "ITEM-403", "name": "Butter Naan", "category": "Bread", "price": 90.00, "ingredients": "Flour, Butter, Milk", "is_vegetarian": True, "spice_level": "None"},
        {"item_id": "ITEM-404", "name": "Tandoori Roti", "category": "Bread", "price": 60.00, "ingredients": "Whole Wheat Flour", "is_vegetarian": True, "spice_level": "None"},
        {"item_id": "ITEM-405", "name": "Jeera Rice", "category": "Rice", "price": 180.00, "ingredients": "Basmati Rice, Cumin Seeds", "is_vegetarian": True, "spice_level": "None"},
        {"item_id": "ITEM-406", "name": "Vegetable Biryani", "category": "Rice", "price": 350.00, "ingredients": "Basmati Rice, Mixed Vegetables, Saffron", "is_vegetarian": True, "spice_level": "Medium"},
        
        # Desserts
        {"item_id": "ITEM-501", "name": "Gulab Jamun (2 pcs)", "category": "Dessert", "price": 100.00, "ingredients": "Milk Solids, Sugar Syrup, Cardamom", "is_vegetarian": True, "spice_level": "None"},
        {"item_id": "ITEM-502", "name": "Rasmalai (2 pcs)", "category": "Dessert", "price": 180.00, "ingredients": "Cottage Cheese, Milk, Saffron", "is_vegetarian": True, "spice_level": "None"},
        {"item_id": "ITEM-503", "name": "Kulfi", "category": "Dessert", "price": 200.00, "ingredients": "Milk, Cardamom, Pistachios", "is_vegetarian": True, "spice_level": "None"},
        {"item_id": "ITEM-504", "name": "Gajar Halwa", "category": "Dessert", "price": 170.00, "ingredients": "Carrot, Milk, Ghee, Sugar", "is_vegetarian": True, "spice_level": "None"},
        
        # Beverages
        {"item_id": "ITEM-601", "name": "Masala Chai", "category": "Beverage", "price": 120.00, "ingredients": "Tea, Milk, Spices", "is_vegetarian": True, "spice_level": "None"},
        {"item_id": "ITEM-602", "name": "Mango Lassi", "category": "Beverage", "price": 180.00, "ingredients": "Mango, Yogurt, Sugar", "is_vegetarian": True, "spice_level": "None"},
        {"item_id": "ITEM-603", "name": "Sweet Lassi", "category": "Beverage", "price": 150.00, "ingredients": "Yogurt, Sugar, Cardamom", "is_vegetarian": True, "spice_level": "None"},
        {"item_id": "ITEM-604", "name": "Fresh Lime Soda", "category": "Beverage", "price": 120.00, "ingredients": "Lime, Soda, Salt/Sugar", "is_vegetarian": True, "spice_level": "None"},
    ]

    # ============================================
    # RESTAURANT MENU ITEMS
    # ============================================
    menu_items_data = []
    restaurants_data = generate_restaurants().to_dict('records')

    df_menu_items = pd.DataFrame(menu_items_data)
    for restaurant in restaurants_data:
        rest_id = restaurant["restaurant_id"]
        
        for item in master_menu:
            price_multiplier = random.uniform(0.95, 1.05)
            
            menu_items_data.append({
                "restaurant_id": rest_id,
                "item_id": item["item_id"],
                "name": item["name"],
                "category": item["category"],
                "price": round(item["price"] * price_multiplier, 2),
                "ingredients": item["ingredients"],
                "is_vegetarian": item["is_vegetarian"],
                "spice_level": item["spice_level"]
            })

    df_menu_items = pd.DataFrame(menu_items_data)
    return df_menu_items

# ============================================
# CUSTOMERS
# ============================================
def generate_customers(n=500):
    customers = []
    
    for i in range(n):
        join_date = fake.date_between(start_date='-2y', end_date='today')
        
        customer = {
            "customer_id": f"CUST-{10000 + i}",
            "name": fake.name(),
            "email": fake.email(),
            "phone": fake.phone_number(),
            "city": random.choice(["Delhi", "Mumbai", "Bengaluru"]),
            "join_date": join_date.strftime("%Y-%m-%d"),
        }
        customers.append(customer)
    
    return pd.DataFrame(customers)


def generate_seed_resturant_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    df_restaurants = generate_restaurants()
    df_menu_items = generate_menu_items()
    df_customers = generate_customers(1000)
    
    df_restaurants.to_csv(os.path.join(script_dir, "data", "restaurants.csv"), index=False)
    df_menu_items.to_csv(os.path.join(script_dir, "data", "menu_items.csv"), index=False)
    df_customers.to_csv(os.path.join(script_dir, "data", "customers.csv"), index=False)

    print(f"Generated {len(df_restaurants)} restaurants")
    print(f"Generated {len(df_menu_items)} menu items")
    print(f"Generated {len(df_customers)} customers")


if __name__ == "__main__":
    generate_seed_resturant_data()