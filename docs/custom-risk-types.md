# Custom Risk Types

It is possible to define a custom risk type that CLI will recognize.
It can be a secret, e.g. an API token, a PII (Personal Identifying Information), or NIL (Non-Inclusive Language)

## File Format

Custom risk type is defined in an YAML file. 

Here is an example file to detect GitLab PAT token:

```yaml
regex:
  value: glpat-[a-zA-Z0-9\-_]{20}
type: gitlab_personal_access_token
category: secret
description: GitLab personal access token
precedence: strong_pattern
```

Field Descriptions:

- **value**: specifies a regular expression to match the risk. Vault Radar supports golang stype regular expressions as well as PCRE
- **type**: unique identifier for the risk type
- **category**: risk category. Must be one of `secret`, `pii`, or `nil` 
- **description**: Human friendly description of the risk type.
- **presence**: This is internal to Vault Radar, use `strong_pattern` for all custom risk types.

More examples:

Non-Inclusive Language