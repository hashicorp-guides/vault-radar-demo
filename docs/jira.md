# `scan-jira` (experimental)
This `vault-radar` command is used for scanning an Atlassian Jira Cloud instance. We currently support scanning the latest version of Jira issue descriptions and all issue comments.

## Authentication
`vault-radar` needs some authentication credentials in order to be able to make requests to the Jira Cloud instance.
### Jira Cloud
This means your instance is hosted by Atlassian, and your instance URL should have ".atlassian.net" in it.

For cloud, there's only one supported patern and it requires an [Atlassian API Token](https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/) and the email of the account that the token belongs to.

In order to provide the information to `vault-radar`, assign the appropriate values to both of these environment variables:
1. `ATLASSIAN_API_TOKEN`
2. `ATLASSIAN_ACCOUNT_EMAIL`

### Jira Server
For self hosted versions of Jira, there are up to 2 different patterns possible.

Jira Software Version 8.14 and higher support [creating a Personal Access Token for a user](https://developer.atlassian.com/server/jira/platform/personal-access-token/). The token will have all the same access rights as the user who creates it. To use the token set the following environment variable to the generated token:
`JIRA_PERSONAL_ACCESS_TOKEN`

Using a personal access token is more secure and should be the preferred access pattern. A personal access token is easier to revoke and regenerate, and generally has a smaller blast radius than a password.

All versions of Jira server supports authorization using the Username (not the email), and Password. To authenticate using these credentials set both of these environment variables:
1. `JIRA_USERNAME`
2. `JIRA_PASSWORD`

## Usage
The following examples all assume you have already set the appropriate environment variable or that you intend to include them as part of the command you run.
### Scan an issue
scan an issue and write the results to an outfile in CSV format, this is the default format for output
```bash
vault-radar scan-jira -u <INSTANCE URL> -i <ISSUE ID> -o <PATH TO OUTPUT>.csv
```
### Scan an issue and output JSON
scan an issue and write the results to an outfile in JSON format
```bash
vault-radar scan-jira -u <INSTANCE URL> -i <ISSUE ID> -o <PATH TO OUTPUT>.json -f json
```
### Scan a Project 
scan a project and write the results to an outfile
```bash
vault-radar scan-jira -u <INSTANCE URL> -p <PROJECT KEY> -o <PATH TO OUTPUT>.csv
```
### Scan using a baseline file
perform a scan using a previous scan's result and write the new changes to an outfile
```bash
vault-radar scan-jira -u <INSTANCE URL> -p <PROJECT KEY> -b <PATH TO BASELINE> -o <PATH TO OUTPUT>.csv
```

### HCP connection scanning behavior

The default behavior of scan commands is to require an HCP cloud connection to scan. This is to ensure that hashes are generated using a shared salt from the cloud keeping consistency across scans. In order to populate the HCP connection information needed you view the docs [here](hcp-upload.md).

To allow for scanning to continue working without the need for HCP cloud connection you can use the new `--offline` flag as such.
```bash
vault-radar scan-jira --offline -u <INSTANCE URL> -p <PROJECT KEY> -o <PATH TO OUTPUT>.csv
```

### Scan using a Vault index file
perform a scan using a generated vault index and write the results to an outfile
```bash
vault-radar scan-jira -u <INSTANCE URL> -p <PROJECT KEY> --index-file <PATH TO VAULT INDEX>.jsonl -o <PATH TO OUTPUT>.csv
```
[How to generate a Vault Index](vault.md#index-generation)
### Scan and restrict the number of secrets found
scan a project and write the results to an outfile and stop scanning when the defined number of secrets are found
```bash
vault-radar scan-jira -u <INSTANCE URL> -p <PROJECT KEY> -o <PATH TO OUTPUT>.csv -l <NUM OF SECRETS>
```
### Scan and restrict the number of issues scanned
scan a project and write the results to an outfile and stop scanning when the defined number of issues has been scanned
```bash
vault-radar scan-jira -u <INSTANCE URL> -p <PROJECT KEY> -o <PATH TO OUTPUT>.csv --issue-limit <NUM OF ISSUES>
```
