import psycopg2
from datetime import datetime, timedelta
conn = psycopg2.connect(host='localhost', database='comparator_prices', user='postgres', password='posgres')
cur = conn.cursor()
now = datetime.now()

cur.execute("INSERT INTO prices (price, discount_price, is_discount, date, product_id, store_id) VALUES (100.00, NULL, false, %s, 1, 1)", (now - timedelta(days=2),))
cur.execute("INSERT INTO prices (price, discount_price, is_discount, date, product_id, store_id) VALUES (95.00, 85.00, true, %s, 1, 1)", (now - timedelta(days=1),))
cur.execute("INSERT INTO prices (price, discount_price, is_discount, date, product_id, store_id) VALUES (105.00, NULL, false, %s, 1, 2)", (now,))

cur.execute("INSERT INTO prices (price, discount_price, is_discount, date, product_id, store_id) VALUES (80.00, NULL, false, %s, 2, 1)", (now - timedelta(days=2),))
cur.execute("INSERT INTO prices (price, discount_price, is_discount, date, product_id, store_id) VALUES (75.00, NULL, false, %s, 2, 2)", (now - timedelta(days=1),))
cur.execute("INSERT INTO prices (price, discount_price, is_discount, date, product_id, store_id) VALUES (70.00, NULL, false, %s, 2, 3)", (now,))

cur.execute("INSERT INTO prices (price, discount_price, is_discount, date, product_id, store_id) VALUES (50.00, NULL, false, %s, 3, 1)", (now - timedelta(days=2),))
cur.execute("INSERT INTO prices (price, discount_price, is_discount, date, product_id, store_id) VALUES (55.00, 45.00, true, %s, 3, 2)", (now,))

conn.commit()
print('Prices inserted')
conn.close()