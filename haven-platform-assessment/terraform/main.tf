# B0 — The `count` trap
#
# Each landlord account gets a dedicated S3 bucket for their media, addressed by POSITION in
# var.landlord_accounts. This is the setup the assignment asks you to reason about: what happens
# to `terraform plan` when an account in the middle of the list is removed?
#
# Try it: this directory ships with a `terraform.tfstate` already seeded with all 4 buckets, so
# you don't need a real AWS account or `terraform apply` to see this. Remove "la-002" from
# variables.tf's default list, then run:
#
#   terraform plan -refresh=false
#
# The -refresh=false matters: a plain `terraform plan` tries to refresh each resource against
# real AWS first, the dummy credentials get a 403, and Terraform quietly drops the "missing"
# resource from state and plans a fresh create instead — which hides the bug entirely. Skipping
# the refresh diffs your config directly against the seeded state, which is what shows the real
# destroy/recreate cascade.

resource "aws_s3_bucket" "landlord_media" {
  count  = length(var.landlord_accounts)
  bucket = "haven-media-${var.landlord_accounts[count.index]}"

  tags = {
    landlord_account_id = var.landlord_accounts[count.index]
  }
}
