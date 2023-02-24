### Question 4 -

Make a Kubernetes deployment strategy which contains an Azure function in python (with source code) which puts a message to Azure Storage Queue every minute.Then make another Azure function that should load a message from a queue and run a prepared container service to print "Hello World".

#### Answer

To create a Kubernetes deployment strategy that includes an Azure Function written in Python which puts a message into an Azure Storage Queue every minute, you can follow these steps:

- First, create an Azure Function App and a Storage Account in Azure.
- In the Function App, create a new Function with an HTTP trigger and Python as the language.
- Add the Python code that will put a message to the Azure Storage Queue every minute. 
- Example:

```python
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
```

- Deploy the Azure Function to Azure using the Azure CLI or Azure Portal.
- Next, create a Dockerfile that contains the necessary commands to prepare a container with a Python environment and the code that will run the Azure Function. 
- Example Dockerfile:
```dockerfile
FROM python:3.7-alpine
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "main.py"]
```
- Build the Docker image and push it to a container registry, such as Azure Container Registry or Docker Hub.
- Create a Kubernetes deployment file that specifies the Docker image to use, the deployment strategy, and the Kubernetes deployment configuration. 
- Example Deployment file:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: azure-function
  labels:
    app: azure-function
spec:
  replicas: 1
  selector:
    matchLabels:
      app: azure-function
  template:
    metadata:
      labels:
        app: azure-function
    spec:
      containers:
      - name: azure-function
        image: <your-container-registry>/<your-image-name>:<your-image-tag>
        env:
        - name: AzureWebJobsStorage
          value: <your-storage-account-connection-string>
        resources:
          limits:
            cpu: 0.5
            memory: "256Mi"
          requests:
            cpu: 0.5
            memory: "256Mi"
```
 - Apply the deployment file to the Kubernetes cluster using the kubectl command.
 
 - To create the second Azure Function that loads a message from the queue and runs a prepared container service to print "Hello World", you can follow these steps:

- Create a new Azure Function in the same Function App with a Queue trigger and Python as the language.
- Add the Python code that will load a message from the queue and run a container service that prints "Hello World". 

- Example:
```python
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
```

- Deploy the Azure Function to Azure using the Azure CLI or Azure Portal.
