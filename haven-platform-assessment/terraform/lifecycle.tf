# B1 — The Glacier cost gotcha
#
# Sold listings' photos archive to Glacier 30 days after upload, to cut storage cost. Separately
# (not modeled in Terraform — it's an application-level flow), a seller can request deletion of
# their listing data, which must happen within 30 days of the request.
#
# Reason through: a photo archives to Glacier on day 30. The seller requests deletion on day 40.
# You delete it immediately. What does that actually cost, given Glacier's minimum storage
# duration, and what would you change here?

resource "aws_s3_bucket" "listing_media" {
  bucket = "haven-listing-media"
}

resource "aws_s3_bucket_lifecycle_configuration" "listing_media_archive" {
  bucket = aws_s3_bucket.listing_media.id

  rule {
    id     = "archive-sold-listing-photos"
    status = "Enabled"

    transition {
      days          = 30
      storage_class = "GLACIER"
    }
  }
}
