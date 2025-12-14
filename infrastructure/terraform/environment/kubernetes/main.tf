module "kubernetes" {
  source                       = "../../modules/kubernetes"
  cloudflare_tunnel_prod_token = var.cloudflare_tunnel_prod_token
}
