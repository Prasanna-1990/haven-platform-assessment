variable "landlord_accounts" {
  type        = list(string)
  description = "Landlord account IDs, in the order their infra was originally provisioned."
  default     = ["la-001", "la-002", "la-003", "la-004"]
}
