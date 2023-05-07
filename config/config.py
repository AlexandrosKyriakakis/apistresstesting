import os

from config.logger import logger


class Env:
    def __init__(self):
        # APP
        self.APP_NAME = 'api-stress-testing'
        self.LOG_LEVEL = 'DEBUG'
        self.ROLE = ''
        self.EXTERNAL_HOST = 'http://example.com'

        # API
        self.API_SERVER_HOST = 'http://api-producer:8000'

        # RED PANDA
        self.RED_PANDA_BROKER_0 = 'redpanda-0:9092'
        self.RED_PANDA_TOPIC = 'test_topic'
        self.RED_PANDA_KEY = b'test_key'
        self.RED_PANDA_CONSUMER_GROUP = 'test_consumer_group'

        # RMQ
        self.RMQ_HOST = 'rabbitmq'
        self.RMQ_QUEUE_NAME = 'test_queue'

        # POSTGRES
        self.DB_HOST = 'db'
        self.DB_NAME = 'metabase'
        self.DB_PORT = '5432'
        self.DB_USER = 'metabase'
        self.DB_PASSWORD = 'db_password'

        self.__get_env_vars()
        return

    def __get_env_vars(self):
        """
        Sets instance variables of the Env class to the values of the corresponding environment variables,
        if they are defined and can be converted to the variable's type. If an environment variable is not defined
        or cannot be converted to the variable's type, the instance variable retains its default value specified
        in the constructor.

        :return: None
        """
        var_names = list(vars(self).keys())
        for var_name in var_names:
            env_var = os.getenv(var_name)
            if env_var is not None:
                var_type = type(getattr(self, var_name))
                try:
                    setattr(self, var_name, var_type(env_var))
                except (TypeError, ValueError) as err:
                    logger.error(
                        'cannot set variable %s of type %s with value %s, error: %s',
                        var_name,
                        var_type,
                        env_var,
                        err,
                    )
                    raise
        return
