# `scan-tfe-variables` (experimental)
This `vault-radar` command is used for scanning non-sensitive variables in a Terraform Cloud/Enterprise organization and identifying variable values that contain sensitive secrets. All non-sensitive variables defined in Variable sets and Workspaces are scanned. Both Terraform and Environment variables are scanned.

## Authentication
`vault-radar` needs some authentication credentials in order to be able to make requests to TFC/TFE
### Terraform Enterprise (TFE)

In order to provide the information to `vault-radar`, specify the following environment variables:
1. `TFE_ADDRESS`
2. `TFE_TOKEN`

### Terraform Cloud (TFC)

For Terraform Cloud, use `https://app.terraform.io` as TFE_ADDRESS


## Usage
The following examples all assume you have already set the appropriate environment variable or that you intend to include them as part of the command you run.

### Scanning variables in all workspaces

Scan all workspaces in a TFC/TFE organization and write the results to a file in CSV format, this is the default format for output. 

```bash
vault-radar scan-tfe-variables --org <TFE ORGANIZATION> -o <PATH TO OUTPUT>.csv
```

### Scanning variables in all workspaces and output in JSON

Scan all workspaces in a TFC/TFE organization and write the results to a file in [JSON Lines](https://jsonlines.org/) format.  

```bash
vault-radar scan-tfe-variables --org <TFE ORGANIZATION> -o <PATH TO OUTPUT>.jsonl -f json
```

### Scanning using a Vault index file

Perform a scan using a generated vault index and write the results to an outfile. 
In this mode, if a risk was previously found in Vault, the scan results will report the location in Vault as well.

```bash
vault-radar scan-tfe-variables --org <TFE ORGANIZATION> -o <PATH TO OUTPUT>.csv --index-file <PATH TO VAULT INDEX>.jsonl
```

### Scan and restrict the number of secrets found

Scan all workspaces in a TFC/TFE organization and write the results to an outfile and stop scanning when the defined number of secrets are found

```bash
vault-radar scan-tfe-variables --org <TFE ORGANIZATION> -o <PATH TO OUTPUT>.csv -l <NUM OF SECRETS>
