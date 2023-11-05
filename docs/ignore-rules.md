# Ignore Rules

It is possible to configure to skip detected risks based on various parameters.
To do that, create a yaml file, see the example below, and put it into path where Vault Radar will be able to find. 

## Where to create the file

For Vault Radar CLI, create `$HOME/.hashicorp/vault-radar/ignore.yaml`

## Example

```yaml
# Ignore by file path
- paths:
    - "**/*_test.go"
    - cli/cmd/default-nil-config.yaml
    - cli/cmd/data/*

# Ignore by secret value
# Equivalent to 'secret_value == my_password OR secret_value == my_token'
- secret_values:
    - my_password
    - my_token

# Ignore by secret type
# Equivalent to 'secret_type == password_assignment OR secret_type == secret_assignment'
- secret_types: [password_assignment, secret_assignment]
```

### Skip by risk file path

To skip risks found in particular files, add the rule to `paths` section. 
Each entry can be a concrete file path or a glob mask.

### Skip by risk value

To skip particular values, add the rule to `secret_values` section. 
Each entry is a regex, if the risk value matches the regex, it will be ignored. 

### Skip by risk type

To skip particular types, add the rule to `secret_types` section.
Each entry is a regex, if the risk value matches the regex, it will be ignored.
