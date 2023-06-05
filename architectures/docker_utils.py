import docker


def get_image(
    docker_client: docker.DockerClient, image_name: str = 'app'
) -> docker.models.images.Image:
    """Get the image if it exists, otherwise build it."""
    try:
        image = docker_client.images.get(image_name)
    except docker.errors.ImageNotFound:
        print('Image not found.')
        # Replace with the path to your Dockerfile
        path_to_dockerfile = '..'

        image, build_logs = docker_client.images.build(
            path=path_to_dockerfile, tag=image_name
        )

        # Print build logs
        for line in build_logs:
            print(line)
    return image


def get_network(
    docker_client: docker.DockerClient, container_name_lookup: str = 'linux'
) -> str:
    """Get the network if it exists, otherwise create it."""
    container = next(
        filter(
            lambda container: container_name_lookup in container.attrs['Name'],
            docker_client.containers.list(),
        )
    )
    network = container.attrs['NetworkSettings']['Networks']
    # check if network exists, otherwise raise error
    network_name = list(network.keys())[0]  # get the first network name
    try:
        network = docker_client.networks.get(network_name)
    except docker.errors.NotFound:
        print('Network not found.')
        raise

    return network_name
