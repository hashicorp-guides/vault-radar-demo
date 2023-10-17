#!/bin/bash
# Copyright (c) HashiCorp, Inc.
# SPDX-License-Identifier: MPL-2.0

DIR="${BASH_SOURCE%/*}"
if [[ ! -d "$DIR" ]]; then DIR="$PWD"; fi
source "$DIR/common-ce.sh"

function kill_vault {
  docker-compose -f "$DIR/vault-ce.yml" down -v

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

  docker-compose -f "$DIR/vault-ce.yml" up -d
  wait_for_up
 
}

function unseal_vault {
  vault_cmd operator unseal "$1"
  sleep 5
}

function restart_vault {
  docker-compose -f "$DIR/vault-ce.yml" restart
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

# Create Vault KVv2 backends
vault_cmd secrets enable -version=2 -path=team1 kv
vault_cmd secrets enable -version=2 -path=team2 kv
vault_cmd secrets enable -version=2 -path=team3 kv
vault_cmd secrets enable -version=2 -path=team4 kv

# Create Vault AppRole backends and roles
vault_cmd auth enable -path=team1-app approle
vault_cmd write -force auth/team1-app/role/foo

vault_cmd auth enable -path=team2-app approle
vault_cmd write -force auth/team2-app/role/bar

vault_cmd auth enable -path=team3-app approle
vault_cmd write -force auth/team3-app/role/baz

vault_cmd auth enable -path=team4-app approle
vault_cmd write -force auth/team4-app/role/quux

# On macOS use `brew install coreutils` to install `gdate`
sudo date -s '-92 days'
restart_vault "$unseal_key"

# Store AWS credentials
aws_access_key_id1=$(yq -r '... comments="" | .samples.aws.[0].aws_access_key_id' "$DIR/../secrets.yaml")
aws_secret_key1=$(yq -r '... comments="" | .samples.aws.[0].aws_secret_key' "$DIR/../secrets.yaml")

vault_cmd kv put team1/aws aws_access_key_id="$aws_access_key_id1" aws_secret_key="$aws_secret_key1"

aws_access_key_id2=$(yq -r '... comments="" | .samples.aws.[1].aws_access_key_id' "$DIR/../secrets.yaml")
aws_secret_key2=$(yq -r '... comments="" | .samples.aws.[1].aws_secret_key' "$DIR/../secrets.yaml")

# Create AppRole secret IDs for team1 and team2
vault write -force auth/team1-app/role/foo/secret-id
vault write -force auth/team2-app/role/bar/secret-id

# On macOS use `brew install coreutils` to install `gdate`
sudo date -s '+10 days'
restart_vault "$unseal_key"

vault_cmd kv put team2/aws aws_access_key_id="$aws_access_key_id2" aws_secret_key="$aws_secret_key2"

aws_access_key_id3=$(yq -r '... comments="" | .samples.aws.[2].aws_access_key_id' "$DIR/../secrets.yaml")
aws_secret_key3=$(yq -r '... comments="" | .samples.aws.[2].aws_secret_key' "$DIR/../secrets.yaml")

# Create AppRole secret ID for team3
vault write -force auth/team3-app/role/baz/secret-id

# On macOS use `brew install coreutils` to install `gdate`
sudo date -s '+10 days'
restart_vault "$unseal_key"

vault_cmd kv put team3/aws aws_access_key_id="$aws_access_key_id3" aws_secret_key="$aws_secret_key3"

vault_cmd kv put team4/aws aws_access_key_id="$aws_access_key_id1" aws_secret_key="$aws_secret_key1"

# On macOS use `brew install coreutils` to install `gdate`
sudo date -s '+72 days'
restart_vault "$unseal_key"

# Store GitHub personal access tokens
vault_cmd kv put team1/github pat="$(yq -r '... comments="" | .samples.github_pats[0]' < "$DIR/../secrets.yaml")"
vault_cmd kv put team2/github pat="$(yq -r '... comments="" | .samples.github_pats[1]' < "$DIR/../secrets.yaml")"
vault_cmd kv put team3/github pat="$(yq -r '... comments="" | .samples.github_pats[2]' < "$DIR/../secrets.yaml")"

# Create AppRole secret ID for team4
vault write -force auth/team4-app/role/quux/secret-id

# reset system clock
sudo sntp -sS time.apple.com

echo "=============================================="
echo "Bootstrap complete:"
echo "Unseal key: $unseal_key"
echo "Root token: $root_token"
echo "=============================================="
