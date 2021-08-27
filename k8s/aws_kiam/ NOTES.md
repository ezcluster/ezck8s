# KIAM

## About the ansible role.

This role wrap the kiam helm chat

The chart is grabbed from the kiam github repo. To update:

- clone this repo
- chekout appropriate tag
- copy helm/kiam content in a folder named by the version in the 'files' role folder.


## Note on current implementation

The kiam server will run on one or several master nodes, which are able to assume all the roles required by all application, this from a dedicated instance role.

The application will run on worker nodes, which have no instance role. But, a kiam agent will be deployed on these nodes, which will proxying all aws STS requests to the server.

This proxying is achieved by setting an iptables rule on worker's nodes, to redirect the `http://169.254.169.254/latest/meta-data/...` requests to the server.

> This IP adress is a specific local link, used by AWS to provide metadata instances.

Note, unlike specified in the documentation, there is no need to set this rule at startup. If the agent is not running, the worker's nodes will not be able to acquire any credential, 
as there is no matching instance role on these nodes.

But, there is a security issue here: If a malicious user is able to launch a POD on one of the control plane node, it will be able to assume any application related role.

## TODO

- Prevent non-admin user to launch a pod on control-plane node (Restrict toleration usage)

