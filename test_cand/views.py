import sqlite3
conn = sqlite3.connect('db.sqlite3')
 
query = "ALTER TABLE 'job_name' RENAME COLUMN 'tester' TO 'Software Tester'"
cur = conn.cursor()
cur.execute(query)
conn.commit()


