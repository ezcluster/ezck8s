
# Add a new version.

The template need just 3 adjustement:

          image: "{{ cert_manager_image_prefix }}quay.io/jetstack/cert-manager-cainjector:v1.10.0"
          image: "{{ cert_manager_image_prefix }}quay.io/jetstack/cert-manager-controller:v1.10.0"
          image: "{{ cert_manager_image_prefix }}quay.io/jetstack/cert-manager-webhook:v1.10.0"


