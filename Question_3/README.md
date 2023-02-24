### Question 3 -

What is a blue/green deployment strategy for Kubernetes based on deployments, service, and ingress. Please describe how to switch versions.

#### Answer

Blue/Green deployment is a deployment strategy where you have two identical environments, one which is currently live (blue), and the other which is not yet live (green). The green environment is updated with a new version of the application or service, and once the new version has been tested and verified to be working correctly, traffic is switched to the green environment.

Here is an example of how to implement Blue/Green deployment strategy for Kubernetes using Deployments, Service, and Ingress.

- Create two identical Deployments, one for the blue environment and one for the green environment. Each deployment will have a unique label to distinguish between them, for example:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-blue
  labels:
    app: myapp
    env: blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      env: blue
  template:
    metadata:
      labels:
        app: myapp
        env: blue
    spec:
      containers:
      - name: myapp
        image: myapp:blue
        ports:
        - containerPort: 80
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-green
  labels:
    app: myapp
    env: green
spec:
  replicas: 0
  selector:
    matchLabels:
      app: myapp
      env: green
  template:
    metadata:
      labels:
        app: myapp
        env: green
    spec:
      containers:
      - name: myapp
        image: myapp:green
        ports:
        - containerPort: 80
```

- Create a Service to load balance traffic to the blue deployment:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp
    env: blue
  ports:
  - name: http
    port: 80
    targetPort: 80
```
- Create an Ingress to expose the service outside the cluster:
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp
spec:
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: myapp
            port:
              name: http
```

- Update the green deployment with the new version of the application:

```cpp
kubectl set image deployment myapp-green myapp=myapp:new-version
```
- Once the green deployment is ready, update the Service to point to the green deployment:

```cpp
kubectl patch service myapp -p '{"spec":{"selector":{"app":"myapp","env":"green"}}}'
```
- Traffic will now be routed to the green deployment, and you can verify that the new version is working correctly. If there are issues, you can switch back to the blue deployment by updating the Service again:

```css
kubectl patch service myapp -p '{"spec":{"selector":{"app":"myapp","env":"blue"}}}'
```

That's how you can switch versions using the Blue/Green deployment strategy in Kubernetes.
