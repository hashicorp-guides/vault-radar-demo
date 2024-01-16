# `scan-confluence`
This `vault-radar` command is used for scanning a Confluence Data Server or Atlassian Confluence Cloud instance.

## Authentication
`vault-radar` needs some authentication credentials in order to be able to make requests to the Confluence instance. The information needed depends on whether you are using Confluence Cloud or Server (self hosted)
### Confluence Cloud
This means your instance is hosted by Atlassian, and your instance URL should have ".atlassian.net" in it.

For cloud, there's only one supported patern and it requires an [Atlassian API Token](https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/) and the email of the account that the token belongs to.

In order to provide the information to `vault-radar`, assign the appropriate values to both of these environment variables:
1. `ATLASSIAN_API_TOKEN`
2. `ATLASSIAN_ACCOUNT_EMAIL`

### Confluence Server
For self hosted versions of Confluence, there are up to 2 different patterns possible.

Versions 7.9 and higher support [creating a Personal Access Token for a user](https://confluence.atlassian.com/enterprise/using-personal-access-tokens-1026032365.html). The token will have all the same access rights as the user who creates it. To use the token set the following environment variable to the generated token:
`CONFLUENCE_PERSONAL_ACCESS_TOKEN`

Using a personal access token is more secure and should be the preferred access pattern. A personal access token is easier to revoke and regenerate, and generally has a smaller blast radius than a password.

All versions of Confluence server supports authorization using the Username (not the email), and Password. To authenticate using these credentials set both of these environment variables:
1. `CONFLUENCE_USERNAME`
2. `CONFLUENCE_PASSWORD`

## Usage
The following examples all assume you have already set the appropriate environment variable or that you intend to include them as part of the command you run.
### Scanning a page
scan a page and write the results to an outfile in CSV format, this is the default format for output
```bash
vault-radar scan-confluence -u <INSTANCE URL> -p <PAGE ID> -o <PATH TO OUTPUT>.csv
```
### Scanning a page and output JSON
scan a page and write the results to an outfile in JSON format
```bash
vault-radar scan-confluence -u <INSTANCE URL> -p <PAGE ID> -o <PATH TO OUTPUT>.json -f json
```
### Scanning a Space
scan a space and write the results to an outfile
```bash
vault-radar scan-confluence -u <INSTANCE URL> -s <SPACE KEY> -o <PATH TO OUTPUT>.csv
```
### Scanning using a baseline file
perform a scan using a previous scan's result and write the new changes to an outfile
```bash
vault-radar scan-confluence -u <INSTANCE URL> -s <SPACE KEY> -b <PATH TO BASELINE> -o <PATH TO OUTPUT>.csv
```
### HCP Upload of Scan Results
To scan confluence and view the results on HCP UI, use the –hcp-upload flag

```bash
vault-radar scan-confluence -u <INSTANCE URL> -s <SPACE KEY> --index-file <PATH TO VAULT INDEX>.jsonl -o <PATH TO OUTPUT>.csv –hcp-upload
```
### Scanning using a Vault index file
perform a scan using a generated vault index and write the results to an outfile
```bash
vault-radar scan-confluence -u <INSTANCE URL> -s <SPACE KEY> --index-file <PATH TO VAULT INDEX>.jsonl -o <PATH TO OUTPUT>.csv
```
[How to generate a Vault Index](vault.md#index-generation)
### Scan and restrict the number of secrets found
scan a space and write the results to an outfile and stop scanning when the defined number of secrets are found
```bash
vault-radar scan-confluence -u <INSTANCE URL> -s <SPACE KEY> -o <PATH TO OUTPUT>.csv -l <NUM OF SECRETS>
```

### Scan the entire history of a space or page (experimental)
All versions of a page or space can be scanned by adding the flag `--with-history`, example:
```bash
vault-radar scan-confluence -u <INSTANCE URL> -s <SPACE KEY> -o <PATH TO OUTPUT>.csv --with-history
```

## Troubleshooting Help

### What's the PageID for my page?
Sometimes you will see the "Pretty" URL which includes the Page Name. If you want the page's ID, in the right corner there should be an options menu for the page. It will usually look like 3 dots `...`. Click on that, and then look for an option like `Page Information` and select that. The URL of the page you land on, should use the PageID in the URL. 

Example:
```
http://localhost:8090/pages/viewinfo.action?pageId=123456
```
`123456` is this example page's ID.

### What's the Space Key for my space or page?
The space key is not always included in the URl of a Page, but it should always be present when selecting the space you are interested in from the main Confluence toolbar. Additionally going to the space's summary details, should explicity define the space key.

Example:
```
http://localhost:8090/display/VSID/Some+Page
```
`VSID` is the space key