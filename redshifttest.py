import psycopg2

try:
    conn = psycopg2.connect(
        host="indiamart.587403180581.eu-north-1.redshift-serverless.amazonaws.com",
        port=5439,
        database="dev",  
        user="admin",    
        password="Rxx9uf7ysu$"
    )
    print("Connection successful!")
    conn.close()
except Exception as e:
    print("Connection failed:", e)
