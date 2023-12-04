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

// Create a generic bucket
resource "aws_s3_bucket" "demo_bucket" {
  bucket = "my-demo-scan-bucket"
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

// Creating a few directories
resource "aws_s3_object" "folder" {
  bucket = aws_s3_bucket.demo_bucket.id
  key    = "test/"
  source = "/dev/null"
  // ToDo: Add windows
}

resource "aws_s3_object" "aws_object" {
  bucket = aws_s3_bucket.demo_bucket.id
  key    = join("", [aws_s3_object.folder.key, "aws_token", ])
  source = "secret-files/aws-token.yaml"
}

resource "aws_s3_object" "azure_object" {
  bucket = aws_s3_bucket.demo_bucket.id
  key    = join("", [aws_s3_object.folder.key, "azure_secret", ])
  source = "secret-files/azure-secret.yaml"
}

resource "aws_s3_object" "folder2" {
  bucket = aws_s3_bucket.demo_bucket.id
  key    = "test2/"
  source = "/dev/null"
}

resource "aws_s3_object" "slack_object" {
  bucket = aws_s3_bucket.demo_bucket.id
  key    = join("", [aws_s3_object.folder2.key, "slack_secret", ])
  source = "secret-files/slack-secrets.yaml"
}


resource "aws_s3_object" "vault_object" {
  bucket = aws_s3_bucket.demo_bucket.id
  key    = join("", [aws_s3_object.folder2.key, "vault_token", ])
  source = "secret-files/vault-token.yaml"
}
