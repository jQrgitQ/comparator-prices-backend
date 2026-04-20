import psycopg2
conn = psycopg2.connect(host='localhost', database='comparator_prices', user='postgres', password='posgres')
cur = conn.cursor()

# More categories
cur.execute("INSERT INTO categories (name) VALUES ('Frutas y Verduras')")
cur.execute("INSERT INTO categories (name) VALUES ('Carnes y Pescados')")
cur.execute("INSERT INTO categories (name) VALUES ('Panaderia')")
cur.execute("INSERT INTO categories (name) VALUES ('Bebidas')")
cur.execute("INSERT INTO categories (name) VALUES ('Snacks')")

conn.commit()
print('Categories inserted')
conn.close()