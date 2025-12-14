variable "k8s_cloudflare_namespace" {
  default = "cloudflare-tunnel"
  type    = string
}
variable "cloudflare_tunnel_prod_token" {
  description = "The Cloudflare Prod Tunnel token for authentication."
  type        = string
  sensitive   = true
}
