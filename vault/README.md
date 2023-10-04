# Vault Testing

## Setup
 We have provided bootstrap scripts for Vault Community Edition and Vault Enterprise, `bootstrap-ce.sh` and `bootstrap-ent.sh`,
respectively. Each script will create a single-node Vault cluster via `docker-compose` then generate multiple KVv2 and
AppRole secrets distributed across multiple mounts. The Vault Enterprise version, `bootstrap-ent.sh`, will spread these
mounts across various namespaces.

The script will start Vault using  `docker-compose -f vault-(ce|ent).yml up -d`. The cluster will then be initialized and
unsealed. The resulting unseal key and root token will be provided via standard out upon completion of the script.

Look for the following:

```bash
==============================================
Bootstrap complete:
Unseal key: <unseal-key>
Root token: <root-token>
==============================================
```

The secrets created will use values from `../sample/secrets.yaml`. The `yq` tool is required to parse these values from
the YAML file. Its GitHub repo provides [installation steps](https://github.com/mikefarah/yq#install) for various systems.
The bootstrap scripts will also change the time of your system clock in order to mimic secrets that have been created in
the past. This is achieved using GNU `date`. If you are using macOS then you will need to run the following to ensure
that you have GNU `date` installed:

```bash
brew install coreutils
```

We have provided `get-secrets-ce.sh` and `get-secrets-ent.sh`, to output the created secrets. You can, of course, add
your own secrets for further testing. Note that the output showcases that a single secret has been shared across multiple teams.

The following will be required to run the `scan-vault` command against the new Vault cluster:

```bash
export VAULT_TOKEN=<token-from-bootstrap-output>
export VAULT_ADDR=http://127.0.0.1:8205
```
