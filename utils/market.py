MARKET_PRICES = {
    "Tomato": 180, "Carrot": 95, "Cabbage": 60, "Brinjal": 120,
    "Leeks": 200, "Bitter Gourd": 150, "Capsicum": 250, "Pumpkin": 75,
    "Potato": 110, "Beetroot": 85, "Spinach": 70, "Radish": 55,
    "Banana": 90, "Papaya": 130, "Mango": 220, "Pineapple": 160,
    "Watermelon": 50, "Avocado": 350, "Guava": 140, "Passion Fruit": 400,
    "Cashew": 1200, "Coconut": 45, "Groundnut": 280, "Macadamia": 1800,
    "Rice": 65, "Maize": 55, "Soybean": 120,
}

PRICE_CHANGES = ["+5.2%", "-2.1%", "+8.4%", "+1.3%", "-0.8%", "+12.1%", "-3.5%", "+4.7%"]

def get_market_data(crops: list) -> list:
    """Return market rows for a list of crop dicts."""
    rows = []
    for i, crop in enumerate(crops):
        name = crop["type"]
        price = MARKET_PRICES.get(name, 100)
        change = PRICE_CHANGES[i % len(PRICE_CHANGES)]
        yield_kg = crop["area"] * 2000
        revenue = round(price * yield_kg / 1000)
        rows.append({
            "crop": name,
            "price": price,
            "change": change,
            "revenue": revenue,
        })
    return rows
