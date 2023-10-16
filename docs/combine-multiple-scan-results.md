# Combine Multiple Scan Results

It might be useful to create a single file with results from multiple different scans. 
The single combined file can be used to look at all scan results at once 
and/or can be passed to other commands as well. 

How to combine the results depends on the format of the results file. 

## JSON

If the output file format is json then combining multiple results is quite simple.
As the format is actually a json-lines, each line is completely independent, 
and it is OK just to concatenate all the result files:

```shell
cat results-1.jsonl results-2.jsonl > combined-results.jsonl
```

Example: scan two different vault clusters and create a combined index 
(see [scan-vault](vault.md) for for information about creating an index)

```shell

VAULT_ADDR=[ADDR1] VAULT_TOKEN=[TOKEN1] vault-radar scan-vault -o vault-index-1.jsonl --index
VAULT_ADDR=[ADDR2] VAULT_TOKEN=[TOKEN2] vault-radar scan-vault -o vault-index-2.jsonl --index

cat vault-index-1.jsonl vault-index-2.jsonl > combined-vault-index.jsonl
```

## CSV

Each CSV file has a header line, so just combining files will not properly work.
To combine a combination of `head` and `tail` commands can be used

```shell
head -n 1 result-1.csv > combined-results.csv && tail -n+2 -q results-1.csv results-2.csv >> combined-results.csv
```

Example: scan two git repos and create a combined file

```shell

vault-radar scan-repo -u <REPO-URL-1> -o scan-repo-results-1.csv
vault-radar scan-repo -u <REPO-URL-2> -o scan-repo-results-2.csv

head -n 1 scan-repo-results-1.csv > combined-results.csv && tail -n+2 -q scan-repo-results-1.csv scan-repo-results-2.csv >> combined-results.csv
```

Note: It only makes sense to combine csv results form the same command, e.g. only results from `scan-repo` command.
Combining results from different commands, e.g. `scan-repo` and `scan-folder` will not properly work
as different commands have different columns. 