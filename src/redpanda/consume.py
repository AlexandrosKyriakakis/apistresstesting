from kafka import KafkaConsumer


def consume(host: str, topics: list[str], group_id: str):
    consumer = KafkaConsumer(
        bootstrap_servers=[host],
        group_id=group_id,
        # auto_offset_reset='earliest',
        enable_auto_commit=False,
        # consumer_timeout_ms=100
    )

    consumer.subscribe(topics)
    yield from consumer


def callback(message):
    topic_info = f'topic: {message.topic} ({message.partition}|{message.offset})'
    message_info = f'key: {message.key}, {message.value}'
    print(f'{topic_info}, {message_info}')


# consume("localhost:19092", ["demo","demo1"], "demo-group2", callback)
