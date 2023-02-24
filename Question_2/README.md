### Question 2 -

How can you restrict networking between pods in Kubernetes? Give an example. Should this
mechanism be enabled separately?

#### Answer 

To restrict networking between pods in Kubernetes, you can use Kubernetes Network Policies. Network Policies are a set of rules that specify how groups of pods are allowed to communicate with each other.

For example, let's say you have two namespaces, "frontend" and "backend", and you want to restrict network traffic between the two namespaces. You can create a Network Policy in the "backend" namespace that only allows incoming traffic from pods with a specific label. Then, you can label the pods in the "frontend" namespace with that specific label to allow them to communicate with pods in the "backend" namespace.

Here's an example of a Network Policy that allows incoming traffic from pods with the label "access: allowed":

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: backend-policy
  namespace: backend
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          access: allowed


```
To enable Network Policies in a Kubernetes cluster, you need to ensure that a network policy controller is installed and running. The most common network policy controller is the Calico network policy controller, but there are others available as well. The exact method for enabling the network policy controller will depend on the specific Kubernetes distribution or environment that you are using.

Once the network policy controller is running, you can create and apply Network Policies to restrict network traffic between pods as needed.
