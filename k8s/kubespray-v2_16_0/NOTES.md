## Notes on cluster_name


cluster_name is used both as the cluster name and the dns internal suffix

In k8s-cluster.yaml:

dns_domain: "{{ cluster_name }}"

Breaking this is a big risk, as it seemes assumed both value should be equals. 
For example, there is some '...svc.{{ cluster_name }}' (which should be '...svc.{{ dns_domain }}' in the playbooks.

Another trap is to provide a name which will not allow to make distinction between internal and external name.

For example, naming a cluster cluster1.infra1 while node will be named nX.cluster1.infra1 and ingress external name ???.ingress.cluster1.infra1. 
This will have for consequence a pod will not be able to access services using external name (As they will not resolve).


