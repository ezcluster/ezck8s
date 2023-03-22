
- Update latest topolvm version
- Handle default deviceClass (Create a storageClass and a flag in lvmd config)


kubectl -n topolvm-system patch serviceaccount default -p '{"imagePullSecrets": [{"name": "image-pull"}]}'


