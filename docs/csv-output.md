# CSV Output Definitions
This page aims to explain and define the various fields that will be present in the CSV output.

## Field Definitions
The following are field definitions that can be present in any CSV output:

| Field Name | Description |
| --- | --- |
| **Category**| This is the type of risk found by Vault Radar. Eg. secret, PII, or NIL.
| **Description**| This is a short human readable description or explanation of the risk.
| **Created At**| This is the time the risk was created or introduced.
| **Author**| This is the user associated with creating or introducing the risk.
| **Severity**| This is a classification of the risk. **Critical** risks are things Vault Radar believe are the most deserving of user's immediate attention, followed by **High**, **Medium**, and **Info**.
| **Is Historic**| This means the risk was both, first created in version that precedes the most recent version and that the risk is not present in the most recent version of the content.
| **Deep Link**| This is a link the content where the risk was found.
| **Value Hash**| This is a hash of the secret value itself. This is NOT the value of the secret. Identical hashes, means the secret values are identical.
| **Fingerprint**| This is a value that is used to distinguish different risk events and incorporates time and location into the value's generation. This is a value that is useful when depending on the output as part of some integration or automation.
| **Textual Context**| This is sometimes populated when Vault Radar identifies a secret value within some text. It can be helpful when trying to find a secret in a page or if there multiple secrets on a page.
| **Activeness**| Vault Radar will attempt to determine if a secret is active or inactive. In the cases where Vault Radar can definitively say a secret is active or inactive the column will populated. In all other cases the column will not be populated to indicate that the status is unknown.
| **Tags**| These are human readable context tags that may provide some additional information about a risk.
| **Managed Location**| This is populated only when scanning with an index file. When the column is populated, that means a secret that is currently in the managed store, was also found in whatever was being scanned. The value will be the location of the secret in the managed store.
| **Managed Location Is Latest**| This is populated only when scanning with an index file. When this column is true, it means the secret that was found is the current version of the secret in the secret manager.
| **Total Managed Locations**| This is populated only when scanning with an index file. This is the number of times a particular risk was found in secrets manager

## Data Source Specific Fields
The following are field definitions for fields that will be present when scanning specific data sources.

### Github
| Field Name | Description |
| --- | --- |
| **Git Reference**| This is the git reference value where the risk was introduced.

### AWS Parameter Store
| Field Name | Description |
| --- | --- |
| **Version**| This is version of the parameter where the risk was introduced.
| **AWS Account ID**| This is the account id associated with the version of the parameter where the risk was introduced.

### S3
| Field Name | Description |
| --- | --- |
| **AWS Account ID**| This is the account id associated with the version of the parameter where the risk was introduced.