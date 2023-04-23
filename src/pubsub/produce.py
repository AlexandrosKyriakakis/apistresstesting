from kafka import KafkaProducer

from config.config import Env


def produce(topic: str, key: bytes, data: bytes, cfg: Env):
    producer = KafkaProducer(bootstrap_servers=cfg.RED_PANDA_BROKER_0)
    # Produce asynchronously
    producer.send(topic, key=key, value=data)
    producer.flush()


def produce_batch(topic: str, l: list[dict], cfg: Env):
    producer = KafkaProducer(bootstrap_servers=cfg.RED_PANDA_BROKER_0)
    # Produce asynchronously
    for kd in l:
        producer.send(
            topic,
            key=kd['key'],
            value=kd['data'],
        )
    producer.flush()
