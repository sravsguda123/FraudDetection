import mysql.connector
from kafka import KafkaProducer
import json
import time

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Connect to MySQL
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="payments_db"
    )

# Fetch new transactions
def fetch_transactions(cursor, last_id):
    cursor.execute(f"SELECT id, amount, status FROM transactions WHERE id > {last_id} ORDER BY id ASC LIMIT 5")
    return cursor.fetchall()

# Send transactions to Kafka
last_transaction_id = 0  # Track last processed transaction

while True:
    try:
        db = connect_db()
        cursor = db.cursor(dictionary=True)

        transactions = fetch_transactions(cursor, last_transaction_id)
        for txn in transactions:
            producer.send('payments', value=txn)
            print(f"Sent: {txn}")
            last_transaction_id = txn["id"]  # Update last processed ID

        cursor.close()
        db.close()
    except Exception as e:
        print(f"Error: {e}")

    time.sleep(5)  # Fetch every 5 seconds

