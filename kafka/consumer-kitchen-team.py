import json
from mongo.connection import get_collection

from confluent_kafka import Consumer

consumer_config = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "kitchen-team",
    "auto.offset.reset": "earliest"
}

consumer = Consumer(consumer_config)

consumer.subscribe(["pizza-orders"])

print("🟢 Consumer is running and subscribed to pizza-orders topic")

try:
    while True:
        msg = consumer.poll(15.0)
        if msg is None:
            continue
        if msg.error():
            print("❌ Error:", msg.error())
            continue

        value = msg.value().decode("utf-8")
        order = json.loads(value)
        # print(f"📦 Received order: {order['quantity']} x {order['item']} from {order['user']}")
except KeyboardInterrupt:
    print("\n🔴 Stopping consumer")

finally:
    consumer.close()


collection = get_collection()

query_filter = { "order_id": order.order_id }
update_operation = {
    "$set": { "status": "DELIVERED" }}