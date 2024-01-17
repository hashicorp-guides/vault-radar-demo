# `scan-aws-s3` (experimental)

This `vault-radar` command is used for scanning an AWS S3 bucket.

## Authentication

`scan-aws-s3` needs permissions to list and get the objects in the bucket, see this simplified [policy document](./scan-aws-s3-policy.json).
The `Resource` in the policy can be limited to the the buckets that one wants to scan.
Refer [AWS authentication document](./aws-authentication.md) for various ways to set up the auth.

## Usage

### Scan all objects in a bucket

To scan all objects within a bucket and write the results to a CSV file (default format)

```bash
vault-radar scan-aws-s3 --bucket <BUCKET NAME> -r <REGION CODE> -o <PATH TO OUTPUT>.csv
```

### Scan all objects in a bucket and output in JSON

To scan all objects within a bucket and write the results in [JSON Lines](https://jsonlines.org/) format

```bash
vault-radar scan-aws-s3 --bucket <BUCKET NAME> -r <REGION CODE> -o <PATH TO OUTPUT>.jsonl -f json
```

### Scan all objects in a bucket with prefix

To scan all objects within a bucket beginning with a prefix

```bash
vault-radar scan-aws-s3 --bucket <BUCKET NAME> -r <REGION CODE> --prefix <PREFIX> -o <PATH TO OUTPUT>.jsonl -f json
```

### Scanning using a baseline file

Perform a scan using a previous scan's result and write the new changes to an outfile.
With `-b` option, only new risks, risks that were not found in the previous scan will be reported.  

```bash
vault-radar scan-aws-s3 --bucket <BUCKET NAME> -r <REGION CODE> -b <PATH TO BASELINE>.csv -o <PATH TO OUTPUT>.csv
```

Note: it is expected that previous and current scans are "similar", 
e.g. both either latest version or history scans and same output format

### Scanning using a Vault index file

Perform a scan using a generated vault index and write the results to an outfile. 
In this mode, if a risk was previously found in Vault, the scan results will report the location in Vault as well.

```bash
vault-radar scan-aws-s3 --bucket <BUCKET NAME> -r <REGION CODE> -o <PATH TO OUTPUT>.csv --index-file <PATH TO VAULT INDEX>.jsonl
```

### Scan and restrict the number of secrets found

To stop scanning when the defined number of secrets are found

```bash
vault-radar scan-aws-s3 --bucket <BUCKET NAME> -r <REGION CODE> -o <PATH TO OUTPUT>.csv -l <NUM OF SECRETS>
```

### Scan and restrict the number of objects scanned

To stop scanning when the defined number of objects are scanned

```bash
vault-radar scan-aws-s3 --bucket <BUCKET NAME> -r <REGION CODE> -o <PATH TO OUTPUT>.csv --object-limit <NUM OF OBJECTS>
```
