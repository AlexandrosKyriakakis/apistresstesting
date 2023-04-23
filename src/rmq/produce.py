def produce(chan, queue_name: str, data: bytes):
    chan.basic_publish(exchange='', routing_key=queue_name, body=data)
