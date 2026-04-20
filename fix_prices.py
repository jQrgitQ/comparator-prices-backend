import psycopg2
conn = psycopg2.connect(host='localhost', database='comparator_prices', user='postgres', password='posgres')
cur = conn.cursor()

# Obtener stores
cur.execute("SELECT id, name FROM stores")
stores = {name: id for id, name in cur.fetchall()}
print("Stores:", stores)

# Añadir precios para los nuevos productos (IDs 6-15)
prices = [
    (100.00, None, False, 6, stores["Walmart"]),
    (95.00, 85.00, True, 6, stores["Costco"]),
    (105.00, None, False, 6, stores["Jumbo"]),
    (80.00, None, False, 7, stores["Walmart"]),
    (75.00, None, False, 7, stores["Costco"]),
    (50.00, None, False, 8, stores["Walmart"]),
    (55.00, 45.00, True, 8, stores["Costco"]),
    (200.00, None, False, 9, stores["Walmart"]),
    (180.00, None, False, 9, stores["Costco"]),
    (150.00, None, False, 10, stores["Walmart"]),
    (45.00, None, False, 11, stores["Walmart"]),
    (55.00, None, False, 12, stores["Walmart"]),
    (30.00, None, False, 13, stores["Walmart"]),
    (250.00, None, False, 14, stores["Walmart"]),
    (220.00, None, False, 15, stores["Walmart"]),
]

for price, discount, is_disc, prod_id, store_id in prices:
    cur.execute("INSERT INTO prices (price, discount_price, is_discount, product_id, store_id) VALUES (%s, %s, %s, %s, %s)", 
               (price, discount, is_disc, prod_id, store_id))

conn.commit()
print("Prices inserted:", len(prices))

conn.close()