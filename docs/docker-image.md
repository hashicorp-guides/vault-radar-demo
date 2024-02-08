# `scan-docker-image` (experimental)
This `vault-radar` command is used for scanning a docker image

## Usage

### Scanning a docker image

Scan a public docker image (or a private image that is already pulled/dowloaded locally) and write the results to a file in CSV format, this is the default format for output. 

Image reference may optionally include a tag. We will scan the latest tag if no tag is specified.

[Docker engine](https://docs.docker.com/engine/install/) is a pre-requisite for scanning docker images using vault-radar. Docker version 24.0 or greater is required.

```bash
vault-radar scan-docker-image -i <IMAGE REFERENCE> -o <PATH TO OUTPUT>.csv
```

### Scanning a private docker image

To scan a private docker image, specify the following environment variables to authenticate against the registry:
1. `DOCKER_REGISTRY_USERNAME`
2. `DOCKER_REGISTRY_PASSWORD`

```bash
vault-radar scan-docker-image -i <IMAGE REFERENCE> -o <PATH TO OUTPUT>.csv
```

Example:
```bash
export DOCKER_REGISTRY_USERNAME=<ARTIFICATORY_USERNAME>
export DOCKER_REGISTRY_PASSWORD=<ARTIFACTORY_TOKEN>
vault-radar scan-docker-image -i XXX.artifactory.XXX/YYY-image -o results-docker-image.csv
```

### Scanning a docker image and output in JSON

Scan a docker image and write the results to a file in [JSON Lines](https://jsonlines.org/) format.  

```bash
vault-radar scan-docker-image -i <IMAGE REFERENCE> -o <PATH TO OUTPUT>.jsonl -f json
```

### HCP connection scanning behavior

The default behavior of scan commands that have `hcp-upload` functionality is to require an HCP cloud connection to scan by default. This is to ensure that hashes are generated using a shared salt from the cloud keeping consistency across scans. In order to populate the HCP connection information needed you view the docs [here](hcp-upload.md).

To allow for scanning to continue working without the need for HCP cloud connection you can use the new `--offline` flag as such.
```bash
vault-radar scan-vault --offline -o <PATH TO OUTPUT>.csv
```

### Scanning using a Vault index file

Perform a scan using a generated vault index and write the results to an outfile. 
In this mode, if a risk was previously found in Vault, the scan results will report the location in Vault as well.

```bash
vault-radar scan-docker-image -i <IMAGE REFERENCE> -o <PATH TO OUTPUT>.csv --index-file <PATH TO VAULT INDEX>.jsonl
```

### Scan and restrict the number of secrets found

Scan a docker image and and write the results to an outfile and stop scanning when the defined number of secrets are found

```bash
vault-radar scan-docker-image -i <IMAGE REFERENCE> -o <PATH TO OUTPUT>.csv -l <NUM OF SECRETS>
```