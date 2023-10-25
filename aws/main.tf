terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

locals {
  yaml_secrets = yamldecode(file("../secrets.yaml"))
  name_prefix = "/demo"
}

# Configure the AWS Provider
provider "aws" {
  region = "us-east-2"
}

// Github Pat Tokens
resource "aws_ssm_parameter" "github_pat" {
  name  = join("/", [local.name_prefix, "github/pat${count.index + 1}", ])
  type  = "String"
  count = 2
  value = local.yaml_secrets.samples.github_pats[count.index]
}

// AWS Creds
resource "aws_ssm_parameter" "aws_secret_creds" {
  name  = join("/", [local.name_prefix, "secret/creds${count.index + 1}", ])
  type  = "String"
  count = 3
  value = "aws_access_key_id=${local.yaml_secrets.samples.aws[count.index].aws_access_key_id} aws_secret_access_key=${local.yaml_secrets.samples.aws[count.index].aws_secret_key}"
}

// Vault Tokens
resource "aws_ssm_parameter" "vault_token" {
  name  = join("/", [local.name_prefix, "vault/token${count.index + 1}", ])
  type  = "String"
  count = 2
  value = local.yaml_secrets.samples.vault_token[count.index]
}

// Gitlab Pat Tokens
resource "aws_ssm_parameter" "gitlab_pats" {
  name  = join("/", [local.name_prefix, "gitlab/pats${count.index + 1}", ])
  type  = "String"
  count = 2
  value = local.yaml_secrets.samples.gitlab_pats[count.index]
}

// Slack tokens as a secret list
resource "aws_ssm_parameter" "slack_secret_list" {
  name  = join("/", [local.name_prefix, "slack/secret/list", ])
  type  = "StringList"
  value = join(",", [local.yaml_secrets.samples.slack_secrets[0], local.yaml_secrets.samples.slack_secrets[1], ])
}

// Not secret example
resource "aws_ssm_parameter" "not_a_secret" {
  name  = join("/", [local.name_prefix, "not/a/secret", ])
  type  = "String"
  value = "test value"
}

// Secure string for indexing
resource "aws_ssm_parameter" "secure_string_example" {
  name  = join("/", [local.name_prefix, "foo/string/secure", ])
  type  = "SecureString"
  value = "bar"
}