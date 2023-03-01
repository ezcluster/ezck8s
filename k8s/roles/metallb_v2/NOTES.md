

# Delete global stuf (CRDs, ClusterRoles)

```
kubectl get crds | grep "metallb.io" | cut -f 1 -d " " | while read a; do echo $a; kubectl delete crd $a; done
```
 
```
kubectl get clusterrolebindings | grep "metallb" | cut -f 1 -d " " | while read a; do echo $a; kubectl delete clusterrolebinding $a; done

kubectl get clusterroles | grep "metallb" | cut -f 1 -d " " | while read a; do echo $a; kubectl delete clusterrole $a; done
```

```
kubectl get ValidatingWebhookConfiguration | grep "metallb" | cut -f 1 -d " " | while read a; do echo $a; kubectl delete ValidatingWebhookConfiguration $a; done
```
