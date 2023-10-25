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

resource "aws_ssm_parameter" "github_pat" {
  name  = join("/", [local.name_prefix, "github/pat", ])
  type  = "String"
  value = local.yaml_secrets.samples.github_pats[0]
}

resource "aws_ssm_parameter" "aws_access_key_id" {
  name  = join("/", [local.name_prefix, "key/id", ])
  type  = "String"
  value = local.yaml_secrets.samples.aws[0].aws_access_key_id
}

resource "aws_ssm_parameter" "aws_secret_key" {
  name  = join("/", [local.name_prefix, "secret/key", ])
  type  = "String"
  value = local.yaml_secrets.samples.aws[0].aws_secret_key
}

resource "aws_ssm_parameter" "vault_token" {
  name  = join("/", [local.name_prefix, "vault/token", ])
  type  = "String"
  value = local.yaml_secrets.samples.vault_token[0]
}

resource "aws_ssm_parameter" "slack_secret_list" {
  name  = join("/", [local.name_prefix, "slack/secret/list", ])
  type  = "StringList"
  value = join(",", [local.yaml_secrets.samples.slack_secrets[0], local.yaml_secrets.samples.slack_secrets[0], ])
}

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