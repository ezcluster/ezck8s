


```
kubectl get crds | grep "cert-manager.io" | cut -f 1 -d " " | while read a; do echo $a; kubectl delete crd $a; done
```
  
```
kubectl get clusterrolebindings | grep "cert-manager" | cut -f 1 -d " " | while read a; do echo $a; kubectl delete clusterrolebinding $a; done

kubectl get clusterroles | grep "cert-manager" | cut -f 1 -d " " | while read a; do echo $a; kubectl delete clusterrole $a; done
```


```
kubectl -n kube-system get role | grep "cert-manager" | cut -f 1 -d " " | while read a; do echo $a; kubectl -n kube-system delete role $a; done

kubectl -n kube-system get rolebinding | grep "cert-manager" | cut -f 1 -d " " | while read a; do echo $a; kubectl -n kube-system delete rolebinding $a; done
```

```
kubectl get MutatingWebhookConfiguration | grep "cert-manager" | cut -f 1 -d " " | while read a; do echo $a; kubectl delete MutatingWebhookConfiguration $a; done

kubectl get ValidatingWebhookConfiguration | grep "cert-manager" | cut -f 1 -d " " | while read a; do echo $a; kubectl delete ValidatingWebhookConfiguration $a; done
```
