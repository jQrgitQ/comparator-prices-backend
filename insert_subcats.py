import psycopg2
conn = psycopg2.connect(host='localhost', database='comparator_prices', user='postgres', password='posgres')
cur = conn.cursor()

# Subcategorías para Lacteos
cur.execute("INSERT INTO subcategories (name, category_id) VALUES ('Leche', 1)")
cur.execute("INSERT INTO subcategories (name, category_id) VALUES ('Yogurt', 1)")
cur.execute("INSERT INTO subcategories (name, category_id) VALUES ('Quesos', 1)")
cur.execute("INSERT INTO subcategories (name, category_id) VALUES ('Mantequilla', 1)")

# Subcategorías para Frutas y Verduras
cur.execute("INSERT INTO subcategories (name, category_id) VALUES ('Frutas', 2)")
cur.execute("INSERT INTO subcategories (name, category_id) VALUES ('Verduras', 2)")
cur.execute("INSERT INTO subcategories (name, category_id) VALUES ('Ensaladas', 2)")

# Subcategorías para Carnes
cur.execute("INSERT INTO subcategories (name, category_id) VALUES ('Pollo', 3)")
cur.execute("INSERT INTO subcategories (name, category_id) VALUES ('Res', 3)")
cur.execute("INSERT INTO subcategories (name, category_id) VALUES ('Pescado', 3)")
cur.execute("INSERT INTO subcategories (name, category_id) VALUES ('Cerdo', 3)")

# Subcategorías para Panadería
cur.execute("INSERT INTO subcategories (name, category_id) VALUES ('Pan', 4)")
cur.execute("INSERT INTO subcategories (name, category_id) VALUES ('Tortillas', 4)")
cur.execute("INSERT INTO subcategories (name, category_id) VALUES ('Pasteles', 4)")

# Subcategorías para Bebidas
cur.execute("INSERT INTO subcategories (name, category_id) VALUES ('Refrescos', 5)")
cur.execute("INSERT INTO subcategories (name, category_id) VALUES ('Jugos', 5)")
cur.execute("INSERT INTO subcategories (name, category_id) VALUES ('Agua', 5)")
cur.execute("INSERT INTO subcategories (name, category_id) VALUES ('Cerveza', 5)")

# Subcategorías para Snacks
cur.execute("INSERT INTO subcategories (name, category_id) VALUES ('Papitas', 6)")
cur.execute("INSERT INTO subcategories (name, category_id) VALUES ('Galletas', 6)")
cur.execute("INSERT INTO subcategories (name, category_id) VALUES ('Chocolates', 6)")

conn.commit()
print('Subcategories inserted')
conn.close()