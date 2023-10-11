# `scan-folder`
This `vault-radar` command is used for scanning a local folder.

## Usage

### Scanning a folder

Scan a folder and write the results to a file in CSV format, this is the default format for output

```bash
vault-radar scan-folder -p <PATH TO FOLDER> -o <PATH TO OUTPUT>.csv
```

### Scanning a folder and output in JSON

Scan a folder and write the results to a file in [JSON Lines](https://jsonlines.org/) format.  

```bash
vault-radar scan-folder -p <PATH TO FOLDER> -o <PATH TO OUTPUT>.jsonl -f json
```

### Scanning using a baseline file

Perform a scan using a previous scan's result and write the new changes to an outfile.
With `-b` option, only new risks, risks that were not found in the previous scan will be reported.  

```bash
vault-radar scan-folder -p <PATH TO FOLDER> -b <PATH TO BASELINE>.csv -o <PATH TO OUTPUT>.csv
```

### Scanning using a Vault index file

Perform a scan using a generated vault index and write the results to an outfile. 
In this mode, if a risk was previously found in Vault, the scan results will report the location in Vault as well.

```bash
vault-radar scan-folder -p <PATH TO FOLDER> -o <PATH TO OUTPUT>.csv --index-file <PATH TO VAULT INDEX>.jsonl
```

### Scan and restrict the number of secrets found

Scan a clone and write the results to an outfile and stop scanning when the defined number of secrets are found

```bash
vault-radar scan-folder -p <PATH TO FOLDER> -o <PATH TO OUTPUT>.csv -l <NUM OF SECRETS>
```

### Modify the secret URI in the output file

By default, the secret URI in the result file will be the full local file path where the secret has been found.
If the results from scan runs on different machines must be combined for further analysis,
--host-name and --path-prefix options could be used.
--host-name specifies the host name to use in secret URI, defaults to local hostname.
--path-prefix specifies the path prefix to use in secret URI. If not specified, then full local path will be used.

```bash
vault-radar scan-folder -p <PATH TO FOLDER> -o <PATH TO OUTPUT>.csv --host-name <HOST NAME> --path-prefix <PATH PREFIX>
```

