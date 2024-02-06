# `scan-slack` (experimental)
This `vault-radar` command is used for scanning Slack channel(s) and identifying messages that contain sensitive secrets. 

## Authentication
`vault-radar` needs some authentication credentials in order to be able to make requests to Slack.
Follow the steps below to generate a User oAuth token and specify the environment variable SLACK_USER_TOKEN to scan Slack channels. 

* [Create a Slack app](https://api.slack.com/start/quickstart#creating)
* [Request scopes](https://api.slack.com/start/quickstart#scopes) Within **OAuth & Permissions** section, scroll down to **Scopes** section.
Under **User Token Scopes**, add scopes: `channels:read`, `channels:history`, `groups:read` and `groups:history`. Note: use **User Token Scopes** and not **Bot Token Scopes**.
*  [Install and Authorize app](https://api.slack.com/start/quickstart#installing)
*  Within **OAuth & Permissions** section, scroll down to **OAuth Tokens for Your Workspace** section, copy the value for **User OAuth Token**

## Usage
The following examples all assume you have already set the appropriate environment variable or that you intend to include them as part of the command you run.

### Scanning messages in all accessible channels

Scan all public and private channels accessible by the Slack app (associated with SLACK_USER_TOKEN) and write the results to a file in CSV format, this is the default format for output.
Default behaviour is to scan messages added in the last day.

```bash
vault-radar scan-slack -o <PATH TO OUTPUT>.csv  --offline
```

### Scanning messages added in the recent past

Scan messages added in the last `<TIME PERIOD>` days to all accessible public and private channels.

```bash
vault-radar scan-slack -t <TIME PERIOD> -o <PATH TO OUTPUT>.csv  --offline
```

### Scanning messages in a specific channel

Scan all messages in a Slack channel and write the results to a file in CSV format.

```bash
vault-radar scan-slack -c <CHANNEL ID> -o <PATH TO OUTPUT>.csv  --offline
```

### Scanning all accessible channels and output in JSON

Scan all accessible public and private channels and write the results to a file in [JSON Lines](https://jsonlines.org/) format.

```bash
vault-radar scan-slack -o <PATH TO OUTPUT>.jsonl -f json --offline
```

### Scanning using a Vault index file

Perform a scan using a generated vault index and write the results to an outfile. 
In this mode, if a risk was previously found in Vault, the scan results will report the location in Vault as well.

```bash
vault-radar scan-slack -o <PATH TO OUTPUT>.csv --index-file <PATH TO VAULT INDEX>.jsonl --offline 
```

### Scan and restrict the number of secrets found

Scan all accessible public and private channels and write the results to an outfile and stop scanning when the defined number of secrets are found

```bash
vault-radar scan-slack -o <PATH TO OUTPUT>.csv -l <NUM OF SECRETS> --offline