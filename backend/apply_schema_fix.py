import sqlite3
c=sqlite3.connect('app.db')
cur=c.cursor()
try:
    cur.execute("ALTER TABLE purchase_orders ADD COLUMN status TEXT DEFAULT 'created'")
    print('added status')
except Exception as e:
    print('status column exists or alter failed:', e)
try:
    cur.execute("ALTER TABLE purchase_orders ADD COLUMN inspection TEXT")
    print('added inspection')
except Exception as e:
    print('inspection column exists or alter failed:', e)
c.commit()
c.close()
print('DONE')
