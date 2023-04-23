from config.logger import logger


def consume(chan, queue_name: str, callback):
    # Start consuming messages from the "hello" queue
    chan.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    logger.info('waiting for RMQ messages')

    # Start the event loop
    chan.start_consuming()
