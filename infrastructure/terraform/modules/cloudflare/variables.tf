variable "cloudflare_account_id" {
  description = "Cloudflare Account Id"
  type        = string
  sensitive   = true
}
variable "cloudflare_api_token" {
  description = "The API token for Cloudflare."
  type        = string
  sensitive   = true
}
