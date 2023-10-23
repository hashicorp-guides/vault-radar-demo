terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = "us-east-2"
}

resource "aws_ssm_parameter" "string_list_example" {
  name  = "/foo/string/list"
  type  = "StringList"
  value = "bar,baz"
}

resource "aws_ssm_parameter" "string_example" {
  name  = "/foo/string"
  type  = "String"
  value = "bar"
}

// Secure string for indexing
resource "aws_ssm_parameter" "secure_string_example" {
  name  = "/foo/string/secure"
  type  = "SecureString"
  value = "bar"
}