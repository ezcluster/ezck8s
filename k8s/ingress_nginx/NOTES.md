

To setup a new version, in the deployment file:

```
      containers:
      - args:
        - /nginx-ingress-controller
{% for cla in ingress_nginx_command_line_arguments %}
        - {{ cla }}
{% endfor %}
        - --election-id=ingress-nginx-leader
        - --controller-class=k8s.io/ingress-nginx
```

```
{% if ingress_nginx_remove_sha %}
        image: {{ingress_nginx_image_prefix}}registry.k8s.io/ingress-nginx/controller:v1.5.1
{% else %}
        image: {{ingress_nginx_image_prefix}}registry.k8s.io/ingress-nginx/controller:v1.5.1@sha256:4ba73c697770664c1e00e9f968de14e08f606ff961c76e5d7033a4a9c593c629
{% endif %}
```

And twice:

```
{% if ingress_nginx_remove_sha %}
        image: {{ingress_nginx_image_prefix}}registry.k8s.io/ingress-nginx/kube-webhook-certgen:v1.5.1
{% else %}
        image: {{ingress_nginx_image_prefix}}registry.k8s.io/ingress-nginx/kube-webhook-certgen:v20220916-gd32f8c343@sha256:39c5b2e3310dc4264d638ad28d9d1d96c4cbb2b2dcfb52368fe4e3c63f61e10f
{% endif %}
```


