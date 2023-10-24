terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

locals {
  yaml_secrets= yamldecode(file("../secrets.yaml"))
}

# Configure the AWS Provider
provider "aws" {
  region = "us-east-2"
}

resource "aws_ssm_parameter" "github_pat" {
  name  = "/github/pat"
  type  = "String"
  value = local.yaml_secrets.samples.github_pats[0]
}

resource "aws_ssm_parameter" "aws_access_key_id" {
  name  = "/test/key/id"
  type  = "String"
  value = local.yaml_secrets.samples.aws[0].aws_access_key_id
}

resource "aws_ssm_parameter" "aws_secret_key" {
  name  = "/test/secret/key"
  type  = "String"
  value = local.yaml_secrets.samples.aws[0].aws_secret_key
}

resource "aws_ssm_parameter" "vault_token" {
  name  = "/vault/token"
  type  = "String"
  value = local.yaml_secrets.samples.vault_token[0]
}

resource "aws_ssm_parameter" "slack_secret_list" {
  name  = "/slack/secret/list"
  type  = "StringList"
  value = join(",", [local.yaml_secrets.samples.slack_secrets[0], local.yaml_secrets.samples.slack_secrets[0],])
}

// Secure string for indexing
resource "aws_ssm_parameter" "secure_string_example" {
  name  = "/foo/string/secure"
  type  = "SecureString"
  value = "bar"
}