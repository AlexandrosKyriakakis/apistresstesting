from kafka import KafkaAdminClient
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError

from config.logger import logger


def create_topics(topic_name: str, host: str):
    admin = KafkaAdminClient(bootstrap_servers=[host])
    try:
        demo_topic = NewTopic(name=topic_name, num_partitions=1, replication_factor=1)
        admin.create_topics(new_topics=[demo_topic])
        logger.info('created topic: %s', topic_name)
    except TopicAlreadyExistsError:
        logger.warn('topic already exists: %s', topic_name)
    finally:
        admin.close()
