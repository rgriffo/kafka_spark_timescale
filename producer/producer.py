from kafka import KafkaProducer
import json
import time
import random

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

for _ in range(10):  # per GitHub Actions: invia solo 10 messaggi
    data = {
        "sensor_id": random.randint(1, 5),
        "temperature": round(random.uniform(20, 30), 2),
        "timestamp": int(time.time())
    }
    producer.send("sensors", value=data)
    time.sleep(1)
