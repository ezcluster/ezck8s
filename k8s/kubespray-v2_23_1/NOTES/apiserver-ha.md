# Kubernetes apiserver high availability

The kubernetes Api Server is the hearth of the cluster. 
In an HA deployment, it will be deployed with several replicas. So, the key point here is to ensure all clients will connect 
to an active replica in all handled case of failure, such as node lost.

This note describe how this is handled in an HA cluster deployed with kubespray.

UPDATE: This note was built from experimental analysis. 
Later on, I found [some doc on this](https://github.com/kubernetes-sigs/kubespray/blob/master/docs/ha-mode.md), 
with far better explanation. 


## Access as a service from inside the cluster

The usual way to reach the apiserver from a pod is to use the `kubernetes` service located in the `default` namespace. 
The IP and port of this service are injected by kubernetes in each pod as environment variable. 
And these values will be used by all k8s client library   

A deeper look find this service is 'special'. For example, there is no pod associated. In fact, no pod selector.

The trick is there is some specific code in the kubernetes master controller to handle it.
You will find more information about this [here](https://networkop.co.uk/post/2020-06-kubernetes-default/)

What is interesting are the associated endpoints:

```
kubectl get endpoints kubernetes
NAME         ENDPOINTS                                                  AGE
kubernetes   192.168.56.30:6443,192.168.56.31:6443,192.168.56.32:6443   74m
```

These endpoints target all the nodes of the control plane. 
With a kubespray deployment, there is an apiserver each of these nodes, bound on port 6443, on the host network.

So, the usual HA mechanism of the service will ensure to reach an active apiserver.

## The bootstrap issue

But this will work fine on a running kubernetes cluster. And a running kubernetes cluster means all kubelets are running.
But to run, a kubelet need to access the apiserver. Usual chicken-and-eggs problem.

The Kubespray solution is to configure all kubelets to reach the apiserver through the localhost network  (127.0.0.1:6443).

Obviously, doing so will solve the problem on the control plane nodes, where there is a bound apiserver (It is bound to all interfaces of the host). 

And for the worker node, kubespray will install a proxy `nginx-proxy` as a pod to redirect request to localhost:6443 to an active apiserver.

Here is an extract of its config:

```
stream {
  upstream kube_apiserver {
    least_conn;
    server 192.168.56.30:6443;
    server 192.168.56.31:6443;
    server 192.168.56.32:6443;
    }

  server {
    listen        127.0.0.1:6443;
    proxy_pass    kube_apiserver;
    proxy_timeout 10m;
    proxy_connect_timeout 1s;
  }
}
```

> This `nginx-proxy` has nothing to do with the ingress controller, which may also be based on nginx. And also nothing to do with the `kube-proxy` present on each node.

This `nginx-proxy` is deployed as a [static pod](https://kubernetes.io/docs/tasks/configure-pod-container/static-pod/), 
thus ensuring it will be started by the kubelet before trying to access the apiserver.

## Access from outside the cluster with metallb

From the outside, the apiserver will be reached directly using the host addresses. We need a loadbalancer in front to ensure we will address an active one.

For this, we can use Metallb to associate a VIP from its pool to the apiserver. Here is a sample manifest :
```
---
apiVersion: v1
kind: Service
metadata:
  name: apiserver-lb
  namespace: kube-system
  annotations:
    metallb.universe.tf/loadBalancerIPs: 192.168.56.42
spec:
  type: LoadBalancer
  selector:
    component: kube-apiserver
    tier: control-plane
  ports:
    - name: https
      protocol: TCP
      port: 443
      targetPort: 6443
```

Then, we can modify the `kubeconfig` file by providing the VIP as the target address, on port 80 

```
    server: https://192.168.56.42
```

But this will not work, due to a certificate issue:

```
Unable to connect to the server: x509: certificate is valid for 10.233.0.1, 192.168.56.31, 192.168.56.30, 127.0.0.1, 192.168.56.32, 10.0.2.15, not 192.168.56.42
```

And setting our own DN name will not solve the problem:

```
Unable to connect to the server: x509: certificate is valid for kubernetes, kubernetes.default, kubernetes.default.svc, kubernetes.default.svc.kspray4.local, lb-apiserver.kubernetes.local, localhost, m0, m0.kspray4, m1, m1.kspray4, m2, m2.kspray4, not apiserver.kspray4
```

So a quick an dirty solution is to use a DN recognized  by the certificate:

```
    server: https://kubernetes.default.svc.kspray4.local
```

And arrange for your DNS to resolve this address to the VIP.

There will be two cleaner solutions:

- Name the kubernetes cluster with a name referencing a DNS subdomain we will manage.
- Modify the server certificate of the apiserver to add our VIP DNS name: TO INVESTIGATE

UPDATE: Found solution. Define `supplementary_addresses_in_ssl_keys` in kubespray. 
[See here](https://github.com/kubernetes-sigs/kubespray/blob/master/docs/ha-mode.md).


A last point: There is an open metallb issue on this topic [here](https://github.com/metallb/metallb/issues/168). 
It states the problem to use metallb as a LB for the apiserver is a bootstrap problem. 
And a workaround would be to configure the kubelet to reach the api server through the localhost. 
Fortunately, as decribed above, this is the way Kubespray build the cluster.




