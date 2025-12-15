resource "cloudflare_zero_trust_tunnel_cloudflared" "k8s_ingress_tunnel_prod" {
  account_id = var.cloudflare_account_id
  name       = "k8s-ingress-tunnel-prod"
  config_src = "cloudflare"
}
