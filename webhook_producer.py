from flask import Flask, request, jsonify
from kafka import KafkaProducer
import json

app = Flask(__name__)

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if data:
        producer.send('payments', value=data)
        print(f"Received transaction: {data}")
    return jsonify({"message": "Received"}), 200

if __name__ == "__main__":
    app.run(port=5000)

