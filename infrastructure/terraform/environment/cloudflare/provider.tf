provider "cloudflare" {
  api_token = var.cloudflare_api_token
}

terraform {
  required_version = ">= 1.3.0"

  required_providers {
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 5.14.0"
    }
  }
}
