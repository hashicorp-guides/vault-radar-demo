terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.28.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = "us-east-2"
}

locals {
  folder_prefix  = "test"
  folder_prefix2 = "test2"
}

resource "random_string" "random_prefix" {
  length = 8
  special = false
  upper = false
}

// Create a generic bucket
resource "aws_s3_bucket" "demo_bucket" {
  bucket = join("-", [random_string.random_prefix.result, "my-demo-scan-bucket", ])
}

resource "aws_s3_object" "github_object" {
  bucket = aws_s3_bucket.demo_bucket.id
  key    = "github_object"
  source = "secret-files/github-pats.yaml"
}

resource "aws_s3_object" "gitlab_object" {
  bucket = aws_s3_bucket.demo_bucket.id
  key    = "gitlab_object"
  source = "secret-files/gitlab-pats.yaml"
}

resource "aws_s3_object" "aws_object" {
  bucket = aws_s3_bucket.demo_bucket.id
  key    = join("/", [local.folder_prefix, "aws_token", ])
  source = "secret-files/aws-token.yaml"
}

resource "aws_s3_object" "azure_object" {
  bucket = aws_s3_bucket.demo_bucket.id
  key    = join("/", [local.folder_prefix, "azure_secret", ])
  source = "secret-files/azure-secret.yaml"
}

resource "aws_s3_object" "slack_object" {
  bucket = aws_s3_bucket.demo_bucket.id
  key    = join("/", [local.folder_prefix2, "slack_secret", ])
  source = "secret-files/slack-secrets.yaml"
}


resource "aws_s3_object" "vault_object" {
  bucket = aws_s3_bucket.demo_bucket.id
  key    = join("/", [local.folder_prefix2, "vault_token", ])
  source = "secret-files/vault-token.yaml"
}
