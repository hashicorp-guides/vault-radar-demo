# scan-vault

This `vault-radar` command is used for scanning a HashiCorp Vault Community Edition
or Enterprise cluster. Scanning Vault using the `scan-vault` provides compliance reporting and secrets indexing
capabilities.

## Authentication and Authorization
`vault-radar` requires the `VAULT_ADDR` and `VAULT_TOKEN` environment variables in
order to connect to your Vault cluster. The `scan-vault` command will traverse the
full namespace hierarchy. Within each namespace, an attempt to scan every AppRole
and KVv2 mount will be made. Access can be limited via the policies attached to the
token provided. `vault-radar` will attempt to use the following endpoints:

| Mount   | Resource                   | Method | Endpoint |
|---------|----------------------------|--------|------------|
| System  | List namespaces            | `LIST` | [sys/namespaces](https://developer.hashicorp.com/vault/api-docs/system/namespaces#list-namespaces) |
| System  | List auth mounts           | `LIST` | [sys/auth](https://developer.hashicorp.com/vault/api-docs/system/auth#list-auth-methods) |
| System  | List secret mounts         | `LIST` | [sys/mounts](https://developer.hashicorp.com/vault/api-docs/system/mounts#list-mounted-secrets-engines) |
| AppRole | List roles                 | `LIST` |  [auth/:mount-path/role](https://developer.hashicorp.com/vault/api-docs/auth/approle#list-roles) |
| AppRole | List secret ID accessors   | `LIST` | [auth/:mount-path/role/:role_name/secret-id](https://developer.hashicorp.com/vault/api-docs/auth/approle#list-secret-id-accessors) |
| AppRole | Lookup secret ID accessors | `POST` | [auth/:mount-path/role/:role_name/secret-id-accessor/lookup](https://developer.hashicorp.com/vault/api-docs/auth/approle#read-approle-secret-id-accessor) |
| KVv2    | Read KV engine config      | `GET`  | [:mount-path/config](https://developer.hashicorp.com/vault/api-docs/secret/kv/kv-v2#read-kv-engine-configuration) |
| Kvv2    | List secrets               | `LIST` | [:mount-path/metadata/:path](https://developer.hashicorp.com/vault/api-docs/secret/kv/kv-v2#list-secrets) |
| KVv2    | Read secret metadata       | `GET`  | [/:mount-path/metadata/:path](https://developer.hashicorp.com/vault/api-docs/secret/kv/kv-v2#read-secret-metadata) |
| KVv2    | Read secret version        | `GET`  | [/:mount-path/data/:path?version=:version-number](https://developer.hashicorp.com/vault/api-docs/secret/kv/kv-v2#read-secret-version) |

## Compliance Reporting
The `scan-vault` command can be used to detect secrets that need to be rotated to meet organization compliance requirements.
The output will contain entries for AppRole and KVv2 secrets. AppRole secrets will have an entry per secret ID accessor. KVv2
secrets will have an entry per secret sub-key, per version, per KVv2 secret. For example, there will be 6 entries for a
secret with 3 versions that contains an AWS access key ID and secret key. KVv2 secret entries will include a hashed
version of the secret value. We will not have access to AppRole secret ID values as those are only provided upon creation.
Secret hashes can be used as a mechanism to detect that a secret has been sprawled within Vault across multiple entries,
mounts, or namespaces.

The following command will scan Vault providing CSV output with a rotation period of 90 days:

```bash
vault-radar scan-vault -outfile vault-scan.csv -rotation-period=90
```

Secrets with an age greater than 90 days will have `medium` severity and provide a warning of `Secret rotation period has been exceeded`.
Warnings will also be provided if a secret is close to exceeding its expiry period (provided by `-expiry-period`) or if
its number of uses (currently specific to AppRole) is close to 0. Entries with multiple warnings will have a severity of
`high`.

The breadth of a scan can be limited and filtered in multiple ways. Most simply, the `-limit` flag can be used to specify
a maximum number of secrets to scan. There are no ordering guarantees with this flag, however, so it is mostly useful to
capture a quick subset of data as a means to fully understand the output's structure. The output can also be filtered
more directly using one or more of the following flags:

- `-namespace`: Only secrets within this namespace will be present in this namespace. Example: `vault-radar scan-vault -namespace=ns1 ...`
- `-mount-type`: Only secrets within mounts of this type will be present in the output. This flag is namespace and path agnostic. Example: `vault-radar scan-vault -mount-type=approle ...`
- `-mount-path:` Only secrets within mounts of this _relative_ path will be present in the output. This flag is namespace and mount-type agnostic. Example: `vault-radar scan-vault -mount-path=app1 ...`

## Index Generation
You can generate an index of KVv2 secrets from Vault using the `scan-vault` command in index mode:

```bash
scan-vault -outfile </path/to/outfile.jsonl> -index
```

The index output will be JSONL-formatted. There will be an entry per secret sub-key, per version, per KVv2 secret.  For example,
there will be 6 entries for a secret with 3 versions that contains an AWS access key ID and secret key.

Each index entry will contain the following fields:

* `value_hash` - The hashed version of the secret value
* `secret_key` - The underlying sub-key within the Vault secret (e.g. `aws_secret_key`)
* `secret_type` - The of type of secret determined by its key and/or underlying value (e.g.GitHub personal access token, AWS secret key)
* `secret_age_days` - The time elapsed in days since creation
* `location` - A full URL that can be used to retrieve the secret (e.g. `vault://127.0.0.1:8205/v1/eng/team1/app-foo/data/aws?version=1`)

The index can then be used to compare against in other scans. For example, the
following command can be used to run a Confluence scan using a generated Vault index file:

```bash
vault-radar scan-confluence --outfile=confluence.csv --url="http://localhost:8090" --space-key=VRD --index-file=vault.idx
```

An in-memory index keyed off of secret hashes will be generated prior to scanning the source. This index will be used to
annotate whether a risk exists in Vault.

### Generate index file using HCP provided salt
Index files are generated in an "online mode" by default, meaning that the secret hash produced is using a salt that is provided from HCP. This requires the Project Service Principals to be configured for your system as outlined by the [HCP Upload Section](hcp-upload.md). If you do not want to use the index file for HCP upload and visualization you can use the `--offline` flag to use a local hashing salt and not error if the Service Principals are not configured.

```bash
vault-radar scan-vault --index -r <REGION CODE> -o <PATH TO OUTPUT>.jsonl --offline
```

### HCP Vault considerations

In a HCP Vault cluster, the root namespace is restricted and the users will only have access to `admin` namespace and all the child namespaces within it.
For `scan-vault` command to work against a HCP Vault cluster, it is mandatory to set `VAULT_PARENT_NAMESPACE` environment variable to the namespace
that needs to be scanned.

```bash
export VAULT_PARENT_NAMESPACE=admin
vault-radar scan-vault -outfile vault-scan.csv -rotation-period=90
```

The above command will scan all the namespaces within the `admin`, including the `admin` namespace.


Note: The `VAULT_PARENT_NAMESPACE` will also work on Vault Enterprise but it is not mandatory to set.
