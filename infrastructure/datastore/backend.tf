terraform {
  backend "s3" {
    # Replace this with your bucket name!
    bucket         = "terraform-state.david-pw.com"
    key            = "production/services/personal-data-dashboard/s3/terraform.tfstate"
    region         = "us-west-2"
  }
}