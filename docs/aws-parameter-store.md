# `scan-aws-parameter-store` (experimental)

This `vault-radar` command is used for scanning parameters of type `String` and `StringList` AWS Parameter Store.
Note: Parameters of type `SecureString` can be indexed, but will not be scanned as they are secure by definition.

## Authentication

`scan-aws-parameter-store` needs permissions to read the parameter, its history and tags, 
see this simplified [policy document](./scan-aws-parameter-store-policy.json).
Refer [AWS authentication document](./aws-authentication.md) for various ways to set up the auth.

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

### HCP connection scanning behavior

The default behavior of scan commands is to require an HCP cloud connection to scan. This is to ensure that hashes are generated using a shared salt from the cloud keeping consistency across scans. In order to populate the HCP connection information needed you view the docs [here](hcp-upload.md).

To allow for scanning to continue working without the need for HCP cloud connection you can use the new `--offline` flag as such.
```bash
vault-radar scan-aws-parameter-store --offline -r <REGION CODE> -o <PATH TO OUTPUT>.csv
```

### Scan and restrict the number of secrets found

To stop scanning when the defined number of secrets are found

```bash
vault-radar scan-aws-parameter-store -r <REGION CODE> -o <PATH TO OUTPUT>.csv -l <NUM OF SECRETS>
```

### Scan and restrict the number of parameters scanned

To stop scanning when the defined number of parameters are scanned

```bash
vault-radar scan-aws-parameter-store -r <REGION CODE> -o <PATH TO OUTPUT>.csv --parameter-limit <NUM OF PARAMETERS>
```

### Generate an index file
Index files are generated in an "online mode" by default, meaning that the secret hash produced is using a salt that is provided from HCP. This requires the Project Service Principals to be configured for your system as outlined by the [HCP Upload Section](hcp-upload.md). If you do not want to use the index file for HCP upload and visualization you can use the `--offline` flag to use a local hashing salt and not error if the Service Principals are not configured.

```bash
vault-radar scan-aws-parameter-store index -r <REGION CODE> -o <PATH TO OUTPUT>.jsonl --offline
```

#### Generate index file using HCP provided salt
To generate an index file using the `SecureString` parameters

```bash
vault-radar scan-aws-parameter-store index -r <REGION CODE> -o <PATH TO OUTPUT>.jsonl
```

### Consuming an index file
To consume the resulting index file use the `index-file` flag when calling a scan command. E.g.

```bash
vault-radar scan-aws-s3 --bucket <BUCKET NAME> -r <REGION CODE> -o <PATH TO OUTPUT>.csv --index-file <PATH TO INDEX FILE>
```