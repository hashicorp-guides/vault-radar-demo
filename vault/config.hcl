# Copyright (c) HashiCorp, Inc.
<<<<<<< Updated upstream
=======
# SPDX-License-Identifier: MPL-2.0
>>>>>>> Stashed changes

storage "raft" {
  path    = "/vault/file"
  node_id = "vault_1"

}

listener "tcp" {
  address = "0.0.0.0:8205"
  cluster_address = "127.0.0.1:8206"
  tls_disable = "true"
}

cluster_addr = "https://127.0.0.1:8206"
api_addr = "http://0.0.0.0:8205"
cluster_name = "vault_1"

log_level = "debug"
