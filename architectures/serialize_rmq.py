import docker

from architectures.docker_utils import get_image
from architectures.docker_utils import get_network
from config import enum
from config.enum import ARCHITECTURE_RMQ
from src.workers.data_worker.countries import COUNTRIES


def create_workers():
    client = docker.from_env()
    image = get_image(client, 'app')
    network_name = get_network(client, 'linux')

    base_port = 5010

    # Create as many data workers as the Countries
    for port_index, (key, country) in enumerate(COUNTRIES.items()):
        container_name = f'data-worker-{key.lower()}'
        container_port = base_port + port_index
        container = client.containers.run(
            image=image,
            name=container_name,
            detach=True,
            ports={'5000/tcp': container_port},
            environment={
                'ROLE': enum.ROLE_DATA_WORKER,
                'COUNTRY': country,
                'ARCHITECTURE': ARCHITECTURE_RMQ,
            },
            network=network_name,
            command='bash -c "python3 run.py"',
        )

        print(container_name, container.id)

    # Create a Daily Worker
    container = client.containers.run(
        image=image,
        name='daily-worker',
        detach=True,
        ports={'5000/tcp': 5002},
        environment={'ROLE': enum.ROLE_DAILY_WORKER, 'ARCHITECTURE': ARCHITECTURE_RMQ},
        network=network_name,
        command='bash -c "python3 run.py"',
        restart_policy={'Name': 'always'},
    )
    print(container.name, container.id)

    # Create a Weekly Worker
    container = client.containers.run(
        image=image,
        name='weekly-worker',
        detach=True,
        ports={'5000/tcp': 5003},
        environment={'ROLE': enum.ROLE_WEEKLY_WORKER, 'ARCHITECTURE': ARCHITECTURE_RMQ},
        network=network_name,
        command='bash -c "python3 run.py"',
        restart_policy={'Name': 'always'},
    )
    print(container.name, container.id)

    # Create a Monthly Worker
    container = client.containers.run(
        image=image,
        name='monthly-worker',
        detach=True,
        ports={'5000/tcp': 5004},
        environment={
            'ROLE': enum.ROLE_MONTHLY_WORKER,
            'ARCHITECTURE': ARCHITECTURE_RMQ,
        },
        network=network_name,
        command='bash -c "python3 run.py"',
        restart_policy={'Name': 'always'},
    )
    print(container.name, container.id)


if __name__ == '__main__':
    create_workers()
