# Argo-cd Ezcluster plugin

## Post install

Get initial password and change it

```
argocd login argocd.ingress.ksprayX.XXX --username admin --password $(kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d)
argocd account update-password --current-password $(kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d) --new-password admin
argocd login argocd.ingress.ksprayX.XXX --username admin --password admin
```

## Add repo:

```
argocd repo add https://github.com/mycompany/myrepo.git --username "user@mycompany.com" --password xxxx
```



