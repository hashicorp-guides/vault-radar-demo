#!/bin/bash
# Copyright (c) HashiCorp, Inc.
# SPDX-License-Identifier: MPL-2.0

DIR="${BASH_SOURCE%/*}"
if [[ ! -d "$DIR" ]]; then DIR="$PWD"; fi

function vault_cmd {
  docker-compose -f "$DIR/vault-ent.yml" exec -T -e VAULT_ADDR="$VAULT_ADDR" -e VAULT_NAMESPACE="$VAULT_NAMESPACE" -e VAULT_TOKEN="$VAULT_TOKEN" vault-enterprise vault "$@"
}
