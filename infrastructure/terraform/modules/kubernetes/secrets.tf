resource "kubernetes_secret" "k8s_ingress_tunnel_prod_credentials" {
  metadata {
    name      = "k8s-ingress-tunnel-prod-credentials"
    namespace = var.k8s_cloudflare_namespace
  }

  data = {
    token = var.cloudflare_tunnel_prod_token
  }
  type = "Opaque"
}
