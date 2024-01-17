# `scan-file` (experimental)

This `vault-radar` command is used for scanning a file. 
It is similar to [scan-folder](folder.md) command but can scan a single file. 
One difference though is that it can read data from standard input.  

## Usage

### Scanning a file

Scan a file and write the results to a file in CSV format, this is the default format for output

```bash
vault-radar scan-file -p <PATH TO FILE> -o <PATH TO OUTPUT>.csv
```

### Scanning a file and output in JSON

Scan a file and write the results to a file in [JSON Lines](https://jsonlines.org/) format.  

```bash
vault-radar scan-file -p <PATH TO FILE> -o <PATH TO OUTPUT>.jsonl -f json
```

### Read data from stdin

Scan data coming from stdin. 
`--name` parameter can be used to name data coming from stdin, 
and it will be used in secret URI in the output file 

```bash
echo "password abcABC123" | vault-radar scan-file -o <PATH TO OUTPUT>.csv --name <NAME> 
```

### Scanning using a baseline file

Perform a scan using a previous scan's result and write the new changes to an outfile.
With `-b` option, only new risks, risks that were not found in the previous scan will be reported.  

```bash
vault-radar scan-file -p <PATH TO FILE> -b <PATH TO BASELINE>.csv -o <PATH TO OUTPUT>.csv
```

### Scanning using a Vault index file

Perform a scan using a generated vault index and write the results to an outfile. 
In this mode, if a risk was previously found in Vault, the scan results will report the location in Vault as well.

```bash
vault-radar scan-file -p <PATH TO FILE> -o <PATH TO OUTPUT>.csv --index-file <PATH TO VAULT INDEX>.jsonl
```

### Scan and restrict the number of secrets found

Scan a clone and write the results to an outfile and stop scanning when the defined number of secrets are found

```bash
vault-radar scan-file -p <PATH TO FILE> -o <PATH TO OUTPUT>.csv -l <NUM OF SECRETS>
```

