#!/bin/bash

DIR="${BASH_SOURCE%/*}"
if [[ ! -d "$DIR" ]]; then DIR="$PWD"; fi
source "$DIR/common-ent.sh"

echo ""
echo ""
echo "AWS secret entries:"
echo ""
echo "eng/team1/app-foo/aws: $(VAULT_NAMESPACE=eng/team1 vault_cmd kv get -format=json app-foo/aws | jq -rcM .data.data)"
echo "eng/team2/app-foo/aws: $(VAULT_NAMESPACE=eng/team2 vault_cmd kv get -format=json app-bar/aws | jq -rcM .data.data)"
echo "eng/team3/app-foo/aws: $(VAULT_NAMESPACE=eng/team3 vault_cmd kv get -format=json app-baz/aws | jq -rcM .data.data)"
echo "eng/team4/app-foo/aws: $(VAULT_NAMESPACE=eng/team4 vault_cmd kv get -format=json app-quux/aws | jq -rcM .data.data)"
echo ""

echo "Uh oh ... looks like team 4 used team 1's creds"
echo ""
echo ""
echo "GitHub personal access token entries"
echo ""
echo "eng/team1/app-foo/aws: $(VAULT_NAMESPACE=eng/team1 vault_cmd kv get -format=json app-foo/github | jq -rcM .data.data)"
echo "eng/team2/app-foo/aws: $(VAULT_NAMESPACE=eng/team2 vault_cmd kv get -format=json app-bar/github | jq -rcM .data.data)"
echo "eng/team3/app-foo/aws: $(VAULT_NAMESPACE=eng/team3 vault_cmd kv get -format=json app-baz/github | jq -rcM .data.data)"
