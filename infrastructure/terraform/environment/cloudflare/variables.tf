variable "cloudflare_email" {
  description = "The email associated with the Cloudflare account."
  type        = string
  sensitive   = true
}

variable "cloudflare_api_token" {
  description = "The API token for Cloudflare."
  type        = string
  sensitive   = true
}
