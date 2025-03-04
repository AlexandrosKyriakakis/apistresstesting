# Roles
ROLE_RED_PANDA_CONSUMER = 'RED_PANDA_CONSUMER'
ROLE_RED_PANDA_PRODUCER = 'RED_PANDA_PRODUCER'
ROLE_API_CONSUMER = 'API_CONSUMER'
ROLE_API_PRODUCER = 'API_PRODUCER'
ROLE_RMQ_CONSUMER = 'RMQ_CONSUMER'
ROLE_RMQ_PRODUCER = 'RMQ_PRODUCER'

roles = {
    ROLE_RED_PANDA_CONSUMER,
    ROLE_RED_PANDA_PRODUCER,
    ROLE_API_CONSUMER,
    ROLE_API_PRODUCER,
    ROLE_RMQ_CONSUMER,
    ROLE_RMQ_PRODUCER,
}

red_panda_roles = {
    ROLE_RED_PANDA_CONSUMER,
    ROLE_RED_PANDA_PRODUCER,
}

api_roles = {
    ROLE_API_CONSUMER,
    ROLE_API_PRODUCER,
}

rmq_roles = {
    ROLE_RMQ_CONSUMER,
    ROLE_RMQ_PRODUCER,
}

# Workers

ROLE_DATA_WORKER = 'DATA_WORKER'
ROLE_DAILY_WORKER = 'DAILY_WORKER'
ROLE_WEEKLY_WORKER = 'WEEKLY_WORKER'
ROLE_MONTHLY_WORKER = 'MONTHLY_WORKER'
ROLE_INITIATOR = 'INITIATOR'


# Architectures
ARCHITECTURE_NULL = ''
ARCHITECTURE_RMQ = 'RMQ'
ARCHITECTURE_ORCHESTRATOR = 'ORCHESTRATOR'
ARCHITECTURE_ASYNC_ORCHESTRATOR = 'ASYNC_ORCHESTRATOR'
ARCHITECTURE_SERIALISED_ORCHESTRATOR = 'SERIALISED_ORCHESTRATOR'
ARCHITECTURE_REDPANDA = 'REDPANDA'
