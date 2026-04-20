import psycopg2
conn = psycopg2.connect(host='localhost', database='comparator_prices', user='postgres', password='posgres')
cur = conn.cursor()

# Limpiar productos y precios
cur.execute("DELETE FROM prices")
cur.execute("DELETE FROM products")

# Obtener subcategorías
cur.execute("SELECT id, name FROM subcategories ORDER BY id")
subcats = {name: id for id, name in cur.fetchall()}
print("Subcategories:", subcats)

# Nuevos productos con los IDs correctos
products = [
    ("Leche Entera 1L", "Leche entera 1 litro", subcats["Leche"]),
    ("Leche Descremada 500ml", "Leche descremada", subcats["Leche"]),
    ("Yogurt Natural", "Yogurt natural", subcats["Yogurt"]),
    ("Queso Mozzarella", "Queso mozzarella 500g", subcats["Quesos"]),
    ("Mantequilla 200g", "Mantequilla sin sal", subcats["Mantequilla"]),
    ("Manzana Roja", "Manzana roja fresca", subcats["Frutas"]),
    ("Plátano", "Plátano maduro", subcats["Frutas"]),
    ("Lechuga", "Lechuga romana", subcats["Verduras"]),
    ("Pechuga Pollo", "Pechuga de pollo", subcats["Pollo"]),
    ("Bistec Res", "Bistec de res", subcats["Res"]),
]

for name, desc, subcat_id in products:
    cur.execute("INSERT INTO products (name, description, subcategory_id) VALUES (%s, %s, %s)", (name, desc, subcat_id))

conn.commit()

cur.execute("SELECT id, name, subcategory_id FROM products ORDER BY id")
prods = cur.fetchall()
print("Products created:", prods)

# Obtener stores
cur.execute("SELECT id, name FROM stores")
stores = {name: id for id, name in cur.fetchall()}
print("Stores:", stores)

# Añadir precios
prices = [
    (100.00, None, False, 1, stores["Walmart"]),
    (95.00, 85.00, True, 1, stores["Costco"]),
    (105.00, None, False, 1, stores["Jumbo"]),
    (80.00, None, False, 2, stores["Walmart"]),
    (75.00, None, False, 2, stores["Costco"]),
    (50.00, None, False, 3, stores["Walmart"]),
    (55.00, 45.00, True, 3, stores["Costco"]),
]

for price, discount, is_disc, prod_id, store_id in prices:
    cur.execute("INSERT INTO prices (price, discount_price, is_discount, product_id, store_id) VALUES (%s, %s, %s, %s, %s)", 
               (price, discount, is_disc, prod_id, store_id))

conn.commit()
print("Prices inserted:", len(prices))

conn.close()