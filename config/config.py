import logging
import os

logging.basicConfig(level='DEBUG')
logger = logging.getLogger('api-stress-testing')


class Env:
    def __init__(self):
        self.APP_NAME = 'api-stress-testing'
        self.LOG_LEVEL = 'DEBUG'
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
