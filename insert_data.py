import psycopg2
conn = psycopg2.connect(host='localhost', database='comparator_prices', user='postgres', password='posgres')
cur = conn.cursor()

cur.execute("INSERT INTO stores (name, location) VALUES ('Walmart', 'Downtown')")
cur.execute("INSERT INTO stores (name, location) VALUES ('Costco', 'Mall Central')")
cur.execute("INSERT INTO stores (name, location) VALUES ('Jumbo', 'North Zone')")

cur.execute("INSERT INTO products (name, description, subcategory_id) VALUES ('Leche Entera 1L', 'Leche entera 1 litro', 1)")
cur.execute("INSERT INTO products (name, description, subcategory_id) VALUES ('Leche Descremada 500ml', 'Leche descremada', 1)")
cur.execute("INSERT INTO products (name, description, subcategory_id) VALUES ('Yogurt Natural', 'Yogurt natural', 1)")

conn.commit()
print('Data inserted')
conn.close()