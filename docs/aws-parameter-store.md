# `scan-aws-parameter-store`

This `vault-radar` command is used for scanning parameters of type `String` and `StringList` AWS Parameter Store.
Note that we do not scan parameters of type `SecureString` as they are secure by definition.

## Authentication
`scan-aws-parameter-store` command needs credentials in order to authenticate to AWS.
There are multiple ways to configure authentication and they are similar to how
`aws` cli authentication is setup.

### Credentials in environment

Set `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` variables in environment.
For example,

```bash
export AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
export AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

Note: If you are using temporary credentials, `AWS_SESSION_TOKEN` also needs to be set.

Refer: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html

### Named profile in credentials file

`vault-radar` can read credentials from the AWS Credentials file, usually located at `$HOME/.aws/config`.
By default, it looks for a profile with name `default`. However any other profile in the credentials file can be
chosen by setting `AWS_PROFILE` environment variable

Refer: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html#cli-configure-files-using-profiles

### EC2 Instance profile

When running `vault-radar` on an AWS EC2 instance, we can assign an IAM role for the EC2 instance and grant
permissions to read parameters from AWS Parameter Store. 
Create policy using this [policy document](scan-aws-parameter-store-policy.json) and assign it to the role.

These credentials are generally available to the code
running on the instance through the Amazon EC2 metadata service. The `vault-radar` CLI can also use these credentials
to scan the AWS Parameter Store.

Refer: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html


### ECS & EKS

It is also possible to run `vault-radar` as a container in AWS ECS (Elastic Container Service) or AWS EKS (Elastic Kubernetes Service).
We need to create an IAM rule using the same [policy document](scan-aws-parameter-store-policy.json) as above.
For ECS, we need to assign the IAM role to the task. 
For EKS, we need to create an IAM OIDC provider for the cluster and assign the role to a service account.

Refer: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-iam-roles.html
Refer: https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html


## Usage

### Scan latest version of parameters

To scan latest version of all parameters within a region and write the results to a CSV file (default format)

```bash
vault-radar scan-aws-parameter-store -r <REGION CODE> -o <PATH TO OUTPUT>.csv
```

### Scan latest version of parameters and output in JSON

To scan latest version of all parameters within a region and write the results in [JSON Lines](https://jsonlines.org/) format

```bash
vault-radar scan-aws-parameter-store -r <REGION CODE> -o <PATH TO OUTPUT>.jsonl -f json
```

### Scan all versions of parameters

To scan all the available versions of all parameters within a region

```bash
vault-radar scan-aws-parameter-store -r <REGION CODE> -o <PATH TO OUTPUT>.csv --with-history
```

### Scanning using a baseline file

Perform a scan using a previous scan's result and write the new changes to an outfile.
With `-b` option, only new risks, risks that were not found in the previous scan will be reported.  

```bash
vault-radar scan-aws-parameter-store -r <REGION CODE> -b <PATH TO BASELINE>.csv -o <PATH TO OUTPUT>.csv
```

Note: it is expected that previous and current scans are "similar", 
e.g. both either latest version or history scans and same output format

### Scanning using a Vault index file

Perform a scan using a generated vault index and write the results to an outfile. 
In this mode, if a risk was previously found in Vault, the scan results will report the location in Vault as well.

```bash
vault-radar scan-aws-parameter-store -r <REGION CODE> -o <PATH TO OUTPUT>.csv --index-file <PATH TO VAULT INDEX>.jsonl
```

### Scan and restrict the number of secrets found

Scan a clone and write the results to an outfile and stop scanning when the defined number of secrets are found

```bash
vault-radar scan-aws-parameter-store -r <REGION CODE> -o <PATH TO OUTPUT>.csv -l <NUM OF SECRETS>
```
