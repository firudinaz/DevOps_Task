import datetime
import logging
import os
import azure.functions as func
from azure.storage.queue import QueueClient

def main(mytimer: func.TimerInput) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()
    
    # Connect to Azure Storage Queue
    queue_client = QueueClient.from_connection_string(
        os.environ["AzureWebJobsStorage"], "myqueue")
    
    # Add a message to the queue
    message = "Hello from Azure Function at {}".format(utc_timestamp)
    queue_client.send_message(message)
    
    logging.info('Python timer trigger function ran at %s', utc_timestamp)
