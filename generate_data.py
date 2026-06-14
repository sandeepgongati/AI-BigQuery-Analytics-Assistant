import pandas as pd
import random
from datetime import datetime, timedelta

cities = [
    "New York",
    "Chicago",
    "Dallas",
    "Boston",
    "Seattle",
    "San Francisco",
    "Miami",
]

products = [
    "Laptop",
    "Phone",
    "Monitor",
    "Tablet",
    "Keyboard",
    "Mouse",
]

rows = []

for i in range(1, 501):
    city = random.choice(cities)
    product = random.choice(products)

    quantity = random.randint(1, 10)

    price = {
        "Laptop": 1200,
        "Phone": 800,
        "Monitor": 250,
        "Tablet": 600,
        "Keyboard": 80,
        "Mouse": 40,
    }[product]

    revenue = quantity * price

    order_date = (
        datetime(2025, 1, 1)
        + timedelta(days=random.randint(0, 180))
    )

    rows.append(
        [
            i,
            city,
            product,
            quantity,
            revenue,
            order_date.date(),
        ]
    )

df = pd.DataFrame(
    rows,
    columns=[
        "order_id",
        "city",
        "product",
        "quantity",
        "revenue",
        "order_date",
    ],
)

df.to_csv("data/retail_sales.csv", index=False)

print("Dataset created successfully!")
print(df.head())