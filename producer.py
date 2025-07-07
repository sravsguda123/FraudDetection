from kafka import KafkaProducer
import json
import random
import time

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

user_ids = ['userA', 'userB', 'userC', 'userD']

def generate_transaction(transaction_id):
    return {
        "transaction_id": f"txn{transaction_id:04}",
        "user_id": random.choice(user_ids),
        "amount": random.randint(100, 5000)  # Random amount between 100 and 5000
    }

print("Sending transactions to 'payments' topic...\n")

transaction_id = 1
while True:
    transaction = generate_transaction(transaction_id)
    producer.send('payments', value=transaction)
    print(f"Sent: {transaction}")
    transaction_id += 1
    time.sleep(2)  # Wait 2 seconds between transactions

