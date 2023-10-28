locals {
    service_name = "personal-data-dashboard"
}

terraform {
  required_providers {
    aws = {
        source = "hashicorp/aws"
        version = "5.1.0"
    }
  }
}

provider "aws" {

    region = "us-west-2"
    
    default_tags {
        tags = {
            service_name = local.service_name
        }
    }
}

resource "aws_s3_bucket" "personal-data" {
    bucket = "personal-data-dashboard.david-pw.com"
}
