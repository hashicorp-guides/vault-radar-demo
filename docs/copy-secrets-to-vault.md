# `copy-secrets-to-vault`
This `vault-radar` command is used for copying unmanaged secrets discovered in a supported scan into HashiCorp Vault.

## Usage

### Supported Scans

We can copy secrets from scans that support this functionality. Those are currently:

- `scan-folder`
- `scan-aws-s3`

If you'd like additional scan types to be added, please reach out and give us that feedback!

### A quick intro/setting the scene

`copy-secrets-to-vault` copies unmanaged secrets, discovered in a scan, to HashiCorp Vault. As a result, it needs to know which secrets are already vaulted.

It figures this out by looking at the outfile of a previous supported scan that used a Vault index file. For example, if you ran

```bash
vault-radar scan-folder -o scan-folder-outfile --index-file vault-scan-outfile
```

where `vault-scan-outfile` is the result of a `scan-vault`, this command would accept as input `scan-folder-outfile` to understand which secrets need to be vaulted.

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

### Understanding where discovered secrets are Vaulted
Discovered secrets will be placed at `<provided vault mount from --vault-path>/data/copied`, where the `key` is the secret's fingerprint from the `vault-radar` scan, and the value is the raw secret value.

The mapping of `<secret fingerprint>` to `<secret location in Vault>` will be output in the outfile at the location specified by `--outfile, -o`.