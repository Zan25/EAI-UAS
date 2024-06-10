from confluent_kafka import Producer, Consumer, KafkaError
import json

# Kafka configuration
KAFKA_BROKER = 'localhost:9092'  # Adjust to your Kafka broker address

# Producer configuration
producer = Producer({
    'bootstrap.servers': KAFKA_BROKER
})

def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

def send_message(topic, message):
    producer.produce(topic, key=None, value=json.dumps(message), callback=delivery_report)
    producer.flush()

# Consumer configuration
consumer = Consumer({
    'bootstrap.servers': KAFKA_BROKER,
    'group.id': 'my-group',
    'auto.offset.reset': 'earliest'
})

def consume_messages(topic):
    consumer.subscribe([topic])

    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(msg.error())
                break

        print('Received message: {}'.format(msg.value().decode('utf-8')))

    consumer.close()
