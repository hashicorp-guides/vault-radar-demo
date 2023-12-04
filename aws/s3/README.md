# AWS S3 Bucket Testing

## Seeding S3 Sample Data

This guide assumes you have Terraform installed (Terraform >=0.13).

Set the following AWS environment variables:

`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` and optionally `AWS_SESSION_TOKEN`.

Additionally, set the `AWS_REGION` environment variable to override the configured region in Terraform: `us-east-2`

Run the following commands to seed s3 data to your AWS account. This will create a new S3 bucket and add several objects.

```
terraform init
terraform apply
```

> **_NOTE:_**  Optionally use `terraform plan` to preview changes before apply.

To delete your test secrets run:

`terraform destroy`