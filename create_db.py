import psycopg2

conn = psycopg2.connect(database="flask_users",  
                        user="gaurishsharma", 
                        password="password",  
                        host="localhost", 
                        port="5432") 
  
cur = conn.cursor() 

cur.execute("SHOW DATABASES")
for db in cur:
    print(db)
  
conn.commit() 
  
cur.close() 
conn.close() 