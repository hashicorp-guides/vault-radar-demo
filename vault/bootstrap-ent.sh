#!/bin/bash
# Copyright (c) HashiCorp, Inc.
<<<<<<< Updated upstream
=======
# SPDX-License-Identifier: MPL-2.0
>>>>>>> Stashed changes


DIR="${BASH_SOURCE%/*}"
if [[ ! -d "$DIR" ]]; then DIR="$PWD"; fi
source "$DIR/common-ent.sh"

function kill_vault {
  docker-compose -f "$DIR/vault-ent.yml" down -v

  while vault_cmd status > /dev/null; do
    echo "Waiting for Vault to stop"
    sleep 1
  done
}

function wait_for_up {
  vault_cmd status > /dev/null

  while [ $? -ne 2 ]; do
    echo "Waiting for Vault to start"
    sleep 1

    vault_cmd status > /dev/null
  done

  echo "Vault is ready!"
}

function start_vault {
  kill_vault

  docker-compose -f "$DIR/vault-ent.yml" up -d
  wait_for_up
 
}

function unseal_vault {
  vault_cmd operator unseal "$1"
  sleep 5
}

function restart_vault {
  docker-compose -f "$DIR/vault-ent.yml" restart
  wait_for_up

  unseal_vault "$1"
  sleep 5
}

export VAULT_ADDR='http://0.0.0.0:8205'

start_vault

# initialize and get unseal key and root token
init_json=$(vault_cmd operator init -key-shares=1 -key-threshold=1 -format=json)

sleep 2

unseal_key=$(echo "$init_json" | jq -r .unseal_keys_hex[0])
root_token=$(echo "$init_json" | jq -r .root_token)

export VAULT_TOKEN="$root_token"

unseal_vault "$unseal_key"
sleep 5

# Create Vault namespaces
vault_cmd namespace create eng

VAULT_NAMESPACE=eng vault_cmd namespace create team1
VAULT_NAMESPACE=eng vault_cmd namespace create team2
VAULT_NAMESPACE=eng vault_cmd namespace create team3
VAULT_NAMESPACE=eng vault_cmd namespace create team4

# Create Vault KVv2 backends
VAULT_NAMESPACE=eng/team1 vault_cmd secrets enable -version=2 -path=app-foo kv
VAULT_NAMESPACE=eng/team2 vault_cmd secrets enable -version=2 -path=app-bar kv
VAULT_NAMESPACE=eng/team3 vault_cmd secrets enable -version=2 -path=app-baz kv
VAULT_NAMESPACE=eng/team4 vault_cmd secrets enable -version=2 -path=app-quux kv

# Create Vault AppRole backends and roles
VAULT_NAMESPACE=eng/team1 vault_cmd auth enable -path=app-foo approle
VAULT_NAMESPACE=eng/team1 vault_cmd write -force auth/app-foo/role/foo

VAULT_NAMESPACE=eng/team2 vault_cmd auth enable -path=app-bar approle
VAULT_NAMESPACE=eng/team2 vault_cmd write -force auth/app-bar/role/bar

VAULT_NAMESPACE=eng/team3 vault_cmd auth enable -path=app-baz approle
VAULT_NAMESPACE=eng/team3 vault_cmd write -force auth/app-baz/role/baz

VAULT_NAMESPACE=eng/team4 vault_cmd auth enable -path=app-quux approle
VAULT_NAMESPACE=eng/team4 vault_cmd write -force auth/app-quux/role/quux

# On macOS use `brew install coreutils` to install `gdate`
sudo date -s '-92 days'
restart_vault "$unseal_key"

# Store AWS credentials
aws_access_key_id1=$(yq -r '... comments="" | .samples.aws.[0].aws_access_key_id' ../secrets.yaml)
aws_secret_key1=$(yq -r '... comments="" | .samples.aws.[0].aws_secret_key' ../secrets.yaml)

VAULT_NAMESPACE=eng/team1 vault_cmd kv put app-foo/aws aws_access_key_id="$aws_access_key_id1" aws_secret_key="$aws_secret_key1"

aws_access_key_id2=$(yq -r '... comments="" | .samples.aws.[1].aws_access_key_id' ../secrets.yaml)
aws_secret_key2=$(yq -r '... comments="" | .samples.aws.[1].aws_secret_key' ../secrets.yaml)

# Create AppRole secret IDs for team1 and team2
VAULT_NAMESPACE=eng/team1 vault write -force auth/app-foo/role/foo/secret-id
VAULT_NAMESPACE=eng/team2 vault write -force auth/app-bar/role/bar/secret-id

# On macOS use `brew install coreutils` to install `gdate`
sudo date -s '+10 days'
restart_vault "$unseal_key"

VAULT_NAMESPACE=eng/team2 vault_cmd kv put app-bar/aws aws_access_key_id="$aws_access_key_id2" aws_secret_key="$aws_secret_key2"

aws_access_key_id3=$(yq -r '... comments="" | .samples.aws.[2].aws_access_key_id' ../secrets.yaml)
aws_secret_key3=$(yq -r '... comments="" | .samples.aws.[2].aws_secret_key' ../secrets.yaml)

# Create AppRole secret ID for team3
VAULT_NAMESPACE=eng/team3 vault write -force auth/app-baz/role/baz/secret-id

# On macOS use `brew install coreutils` to install `gdate`
sudo date -s '+10 days'
restart_vault "$unseal_key"

VAULT_NAMESPACE=eng/team3 vault_cmd kv put app-baz/aws aws_access_key_id="$aws_access_key_id3" aws_secret_key="$aws_secret_key3"

VAULT_NAMESPACE=eng/team4 vault_cmd kv put app-quux/aws aws_access_key_id="$aws_access_key_id1" aws_secret_key="$aws_secret_key1"

# On macOS use `brew install coreutils` to install `gdate`
sudo date -s '+72 days'
restart_vault "$unseal_key"

# Store GitHub personal access tokens
VAULT_NAMESPACE=eng/team1 vault_cmd kv put app-foo/github pat="$(yq -r '... comments="" | .samples.github_pats[0]' < ../secrets.yaml)"
VAULT_NAMESPACE=eng/team2 vault_cmd kv put app-bar/github pat="$(yq -r '... comments="" | .samples.github_pats[1]' < ../secrets.yaml)"
VAULT_NAMESPACE=eng/team3 vault_cmd kv put app-baz/github pat="$(yq -r '... comments="" | .samples.github_pats[2]' < ../secrets.yaml)"

# Create AppRole secret ID for team4
VAULT_NAMESPACE=eng/team4 vault write -force auth/app-quux/role/quux/secret-id

# reset system clock
sudo sntp -sS time.apple.com

echo "=============================================="
echo "Bootstrap complete:"
echo "Unseal key: $unseal_key"
echo "Root token: $root_token"
echo "=============================================="
