# AWS Parameter Store Testing

## Seeding Parameter Store Sample Data

This guide assumes you have Terraform installed.

Set the following AWS environment variables:

`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` and optionally `AWS_SESSION_TOKEN`.

Additionally, set the `AWS_REGION` environment variable to override the configured region in Terraform: `us-east-2`

Run the following commands to seed parameter store data to your AWS account.

```
terraform init
terraform apply
```

To delete your test secrets run:

`terraform destroy`
