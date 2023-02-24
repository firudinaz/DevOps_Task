### Question 4 -

Make a Kubernetes deployment strategy which contains an Azure function in python (with source code) which puts a message to Azure Storage Queue every minute.Then make another Azure function that should load a message from a queue and run a prepared container service to print "Hello World".

#### Answer


- Create a Python Azure function to put a message to the Azure Storage Queue every minute. You can use the Azure SDK for Python to interact with Azure Storage Queue. Here's an example of the function code:

```python
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
```

- Create a Docker container image that contains the service you want to run when a message is loaded from the queue. For this example, let's say the container runs a simple Python script that prints "Hello World". Here's an example Dockerfile:

```dockerfile
FROM python:3.9
COPY script.py .
CMD ["python", "script.py"]
```

- Create a Kubernetes deployment strategy that includes the two functions and the container service. Here's an example of the deployment YAML:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 1
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: function-put
        image: myfunctionput:latest
        env:
        - name: AzureWebJobsStorage
          valueFrom:
            secretKeyRef:
              name: mysecrets
              key: AzureWebJobsStorage
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 200m
            memory: 256Mi
      - name: function-load
        image: myfunctionload:latest
        env:
        - name: AzureWebJobsStorage
          valueFrom:
            secretKeyRef:
              name: mysecrets
              key: AzureWebJobsStorage
        - name: AzureFunctionsJobHost__functions__0
          value: QueueTrigger
        - name: AzureFunctionsJobHost__functions__0__type
          value: queueTrigger
        - name: AzureFunctionsJobHost__functions__0__direction
          value: in
        - name: AzureFunctionsJobHost__functions__0__queueName
          value: myqueue
        - name: AzureFunctionsJobHost__functions__0__connection
          value: AzureWebJobsStorage
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 200m
            memory: 256Mi
      - name: container-service
        image: mycontainerservice:latest
        env:
        - name: MESSAGE
          value: "Hello World"
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 200m
            memory: 256Mi
---
apiVersion: v1
kind: Service
metadata:
```

