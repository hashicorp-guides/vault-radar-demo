# `scan-repo`
This `vault-radar` command is used for scanning a git repo.

## Authentication
`scan-repo` command can either scan an existing repo clone or automatically clone the repo using provided repo url.
If existing clone is used, then no authentication needed. 
If a repo is public, then no authentication is needed.
Otherwise, a git token must be provided, so CLI can clone the repo.
CLI will read the token from `VAULT_RADAR_GIT_TOKEN` environmental variable.
The environmental variable value depends on git server provider. 
For GitHub and GitLab it can be just a personal access token (PAT).
For BitBucket and Azure DevOps, it should be in format `<username>:<PAT>`.

Note: internally CLI uses https:// to clone the repo and ot sets HTTP `username:password` part of the clone URL 
to the value of `VAULT_RADAR_GIT_TOKEN`. Contact your git server provider documentation about the exact format used for 
https:// auth in case the format described above does not work. 

Note 2: For GitHub repos (with 'github' as part of repo url), CLI will use `GITHUB_TOKEN` variable if it exists. 

## Usage

### Scanning a clone

Scan a repo (clone) and write the results to a file in CSV format, this is the default format for output

```bash
vault-radar scan-repo -c <PATH TO CLONE DIR> -o <PATH TO OUTPUT>.csv
```

Note 1: to properly attribute found risks to git_reference (branch) where risks were introduced,
it is expected that the default branch is checked out or the clone is a bare clone.
If non-default branch is checked out most risks will be attributed to that branch instead.

Note 2: Only risks that are still on tip of that branch will be reported. 

### Scanning a clone and output in JSON

Scan a repo (clone) and write the results to a file in [JSON Lines](https://jsonlines.org/) format.  

```bash
vault-radar scan-repo -c <PATH TO CLONE DIR> -o <PATH TO OUTPUT>.jsonl -f json
```

### Scanning a repo with full history

Automatically clones and scans a repo. All the repo commits will be scanned. 

```bash
vault-radar scan-repo -u <REPO URL> -o <PATH TO OUTPUT>.csv --with-history
```

Note: it is possible to scan commits history with an existing clone as well. 
The difference with the above is that with existing clone only commits available in the clone will be scanned,
not all the repo reachable commits.  
The clone might have much fewer commits than the repo itself, e.g. if the clone is a shallow clone 
or if only a single branch was cloned.
To scan all the reachable commits it is recommended to scan repo using `-u` and `--with-history` parameters.

### HCP connection scanning behavior

The default behavior of scan commands is to require an HCP cloud connection to scan. This is to ensure that hashes are generated using a shared salt from the cloud keeping consistency across scans. In order to populate the HCP connection information needed you view the docs [here](hcp-upload.md).

To allow for scanning to continue working without the need for HCP cloud connection you can use the new `--offline` flag as such.
```bash
vault-radar scan-repo --offline -u <REPO URL> -o <PATH TO OUTPUT>.csv
```

### Scanning using a baseline file

Perform a scan using a previous scan's result and write the new changes to an outfile.
With `-b` option, only new risks, risks that were not found in the previous scan will be reported.  

```bash
vault-radar scan-repo -u <REPO URL> -b <PATH TO BASELINE>.csv -o <PATH TO OUTPUT>.csv
```

Note: it is expected that previous and current scans are "similar", 
e.g. both either clone or repo scans, with or without history, etc.

### HCP Upload of Scan Results
To scan git repository and view the results on HCP UI, use the –hcp-upload flag

```bash
vault-radar scan-repo -c <PATH TO CLONE DIR> -o <PATH TO OUTPUT>.csv --index-file <PATH TO VAULT INDEX>.jsonl –hcp-upload
```

### Scanning using a Vault index file

Perform a scan using a generated vault index and write the results to an outfile. 
In this mode, if a risk was previously found in Vault, the scan results will report the location in Vault as well.

```bash
vault-radar scan-repo -c <PATH TO CLONE DIR> -o <PATH TO OUTPUT>.csv --index-file <PATH TO VAULT INDEX>.jsonl
```

### Scan and restrict the number of secrets found

Scan a clone and write the results to an outfile and stop scanning when the defined number of secrets are found

```bash
vault-radar scan-repo -c <PATH TO CLONE DIR> -o <PATH TO OUTPUT>.csv -l <NUM OF SECRETS>
```

### Scan and restrict the number of commit scanned

Scan a clone and stop scanning when the defined number of commits are scanned

```bash
vault-radar scan-repo -c <PATH TO CLONE DIR> -o <PATH TO OUTPUT>.csv --commit-limit <NUM OF COMMITS> --with-history
```


