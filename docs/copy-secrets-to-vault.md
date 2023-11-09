# `copy-secrets-to-vault` (experimental)
This `vault-radar` command is used for copying unmanaged secrets discovered in a supported scan into HashiCorp Vault.

## Usage

### Supported Scans

We can copy secrets from scans that support this functionality. Those are currently:

- `scan-folder`
- `scan-aws-s3`

If you'd like additional scan types to be added, please reach out and give us that feedback!

### A quick intro/setting the scene

`copy-secrets-to-vault` copies unmanaged secrets, discovered in a scan, to HashiCorp Vault. As a result, it needs to know which secrets are already managed.

It figures this out by looking at the outfile of a previous supported scan that used a Vault index file. For example, if you ran

```bash
vault-radar scan-folder -o scan-folder-outfile --index-file vault-scan-outfile
```

where `vault-scan-outfile` is the result of a `scan-vault`, this command would accept as input `scan-folder-outfile` to understand which secrets need to be managed.

`copy-secrets-to-vault` will then re-run the previous scan (characterized by `scan-folder-outfile` in the above example), gather the unmanaged secrets, and Vault them.

Also note that if the previous scan had a `--limit` specified, that will apply here as well.

### Vault Parameters

`copy-secrets-to-vault` pulls the required vault parameters from environment variables, including the namespace in which to mount the KVv2 mount (from `VAULT_NAMESPACE`).

### Copying secrets to Vault

Re-run the previous scan and copy the unmanaged secrets into a Vault KVv2 mount, specified by `--vault-path, -v`:

```bash
vault-radar copy-secrets-to-vault -p <PATH TO PREVIOUS SCAN OUTFILE> -o <PATH TO OUTPUT>.csv -v <LOCATION TO MOUNT A NEW VAULT KVv2>
```

Note that there must not exist a KVv2 mount at the path specified by `--vault-path, -v`, as this tool will create a new KVv2 mount for discovered secrets.

### Limiting the number of secrets copied

If you would like to limit how many secrets are copied to Vault, you may specify that with `--limit, -l`. This will scan until a maximum of `limit` unmanaged secrets are discovered, and copy over a maximum of `limit` secrets.

To e.g. limit the above scan to 200 results:

```bash
vault-radar copy-secrets-to-vault -p <PATH TO PREVIOUS SCAN OUTFILE> -o <PATH TO OUTPUT>.csv -v <LOCATION TO MOUNT A NEW VAULT KVv2> -l 200
```

### Understanding where discovered secrets are placed in Vault
Discovered secrets will be placed at `<provided vault mount from --vault-path>/data/copied`, where the `key` is the secret's fingerprint from the `vault-radar` scan, and the value is the raw secret value.

The mapping of `<secret fingerprint>` to `<secret location in Vault>` will be output in the outfile at the location specified by `--outfile, -o`.

### Example: copy secrets found in `scan-folder` to Vault

First, we'll run `scan-vault` to understand what secrets are already managed (in Vault). We'll specify that we want to generate an index file, and we'll generate our outfile as `scan-vault-outfile`.

```bash
vault-radar scan-vault -o scan-vault-outfile --index
```

Next, we'll run `scan-folder` to discover leaked secrets in the current directory. We'll provide the index file from the previous `scan-vault` step so that this scan has context on already managed secrets, and we'll specify our outfile as `scan-folder-outfile`.

```bash
vault-radar scan-folder -o scan-folder-outfile --index-file scan-vault-outfile
```

Finally, we'll run `copy-secrets-to-vault` to copy over any secrets found in the previous `scan-folder` step, except for those already managed in Vault. We'll provide `scan-vault-outfile` so that this command can understand which secrets discovered in `scan-folder` are already managed in `vault` (so that we avoid copying those over). We'll copy the unmanaged secrets to a new KVv2 mount at `path/to/test`, and we'll generate our outfile as `copy-secrets-to-vault-outfile`. This outfile allows us to know where previously unmanaged secrets were placed in Vault.

```bash
vault-radar copy-secrets-to-vault -p scan-vault-outfile -o copy-secrets-to-vault-outfile -v path/to/test
```