import time

import docker

from architectures.docker_utils import get_image
from architectures.docker_utils import get_network
from config import config
from config import enum
from config.enum import ARCHITECTURE_REDPANDA
from src.workers.data_worker.countries import COUNTRIES


def create_workers():
    client = docker.from_env()
    image = get_image(client, 'app')
    network_name = get_network(client, 'linux')

    # Create Initiator Worker
    container = client.containers.run(
        image=image,
        name='initiator-worker',
        detach=True,
        environment={
            'ROLE': enum.ROLE_INITIATOR,
            'ARCHITECTURE': ARCHITECTURE_REDPANDA,
        },
        network=network_name,
        command='bash -c "python3 run.py"',
    )

    print(container.name, container.id)

    print(container.wait())

    # Create a Daily Worker
    for i in range(config.Env().PARALLEL_WORKERS):
        container = client.containers.run(
            image=image,
            name='daily-worker-' + str(i),
            detach=True,
            environment={
                'ROLE': enum.ROLE_DAILY_WORKER,
                'ARCHITECTURE': ARCHITECTURE_REDPANDA,
                'RED_PANDA_CONSUMER_GROUP': enum.ROLE_DAILY_WORKER,
            },
            network=network_name,
            command='bash -c "python3 run.py"',
            restart_policy={'Name': 'always'},
        )
        print(container.name, container.id)

    # Create a Weekly Worker
    for i in range(config.Env().PARALLEL_WORKERS):
        container = client.containers.run(
            image=image,
            name='weekly-worker-' + str(i),
            detach=True,
            environment={
                'ROLE': enum.ROLE_WEEKLY_WORKER,
                'ARCHITECTURE': ARCHITECTURE_REDPANDA,
                'RED_PANDA_CONSUMER_GROUP': enum.ROLE_WEEKLY_WORKER,
            },
            network=network_name,
            command='bash -c "python3 run.py"',
            restart_policy={'Name': 'always'},
        )
        print(container.name, container.id)

    # Create a Monthly Worker
    for i in range(config.Env().PARALLEL_WORKERS):
        container = client.containers.run(
            image=image,
            name='monthly-worker-' + str(i),
            detach=True,
            environment={
                'ROLE': enum.ROLE_MONTHLY_WORKER,
                'ARCHITECTURE': ARCHITECTURE_REDPANDA,
                'RED_PANDA_CONSUMER_GROUP': enum.ROLE_MONTHLY_WORKER,
            },
            network=network_name,
            command='bash -c "python3 run.py"',
            restart_policy={'Name': 'always'},
        )
        print(container.name, container.id)

    # Wait for consumer to instantiate
    time.sleep(20)

    # Create as many data workers as the Countries
    for _, (key, country) in enumerate(COUNTRIES.items()):
        container_name = f'data-worker-{key.lower()}'
        container = client.containers.run(
            image=image,
            name=container_name,
            detach=True,
            environment={
                'ROLE': enum.ROLE_DATA_WORKER,
                'COUNTRY': country,
                'ARCHITECTURE': ARCHITECTURE_REDPANDA,
            },
            network=network_name,
            command='bash -c "python3 run.py"',
        )

        print(container_name, container.id)


if __name__ == '__main__':
    create_workers()
