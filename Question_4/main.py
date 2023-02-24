import azure.functions as func
import datetime
import os
from azure.storage.queue import QueueClient

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()

    connection_string = os.environ['AzureWebJobsStorage']
    queue_name = 'myqueue'

    queue_client = QueueClient.from_connection_string(connection_string, queue_name)

    message = 'Message created at: ' + utc_timestamp

    queue_client.send_message(message)
