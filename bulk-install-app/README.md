# Vault Radar Bulk Installation Script for GitHub Checks App

## Requirements
- [python >= 3.6](https://www.python.org/downloads/)
- [python package requests](https://pypi.org/project/requests/)
- [python package python-dotenv](https://pypi.org/project/python-dotenv/)
- [python package beautifulsoup4](https://pypi.org/project/beautifulsoup4/)
## Bulk installing a GitHub Checks App across organizations
1. Navigate to Vault Radar portal, and import the organizations that need to install the GitHub App 
2. In `hashicorp-guides/vault-radar-demo/bulk-install-app`, generate an environment file `.env`, with the following variables set:
   - `GITHUB_USERNAME` - the GitHub user's username
   - `GITHUB_PASSWORD` - the GitHub user's password
   - `GITHUB_DOMAIN` - the domain of the GitHub Enterprise Server 
     (optional: only required for GitHub Enterprise Server)
   - `MAX_ORGANIZATIONS` - maximum number of successful organization installations per run of script 
     (optional: if not set, will install on all organizations)
   - `GITHUB_APP_NAME` - the name of the app
     (optional: if not set, will default to `hashicorp-vault-radar-checks-app`)
3. Run the script with the following command to install: `python3 -u main.py 2>&1 | tee -a bulk-install-app-results.txt`
   Run the script with the following command to uninstall: `python3 -u main.py --uninstall 2>&1 | tee -a bulk-install-app-results.txt`
   NOTE: Only organizations/users that the logged in GitHub user has permissions to install/uninstall on will be installed/uninstalled.
   - If two-factor authentication is enabled, the script will request input for the one-time password.
        
When contacting support, please send over the `bulk-install-app-results.txt` file generated from step 3. 
