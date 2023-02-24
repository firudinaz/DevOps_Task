import os
from azure.storage.queue import QueueClient
import subprocess

def main(msg: str) -> None:
    connection_string = os.environ['AzureWebJobsStorage']
    queue_name = 'myqueue'

    queue_client = QueueClient.from_connection_string(connection_string, queue_name)

    message = queue_client.receive_message()

    container_image = '<your-container-registry>/<your-image-name>:<your-image-tag>'

    subprocess.run(['docker', 'run', container_image, 'echo', 'Hello World!'])
