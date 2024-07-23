# Agent (Private Beta)

A hybrid agent has the capability to scan a resource within your Virtual Private Cloud (VPC) environment based on the inputs provided through the HCP UI.
The `agent` command is used to fetch scan jobs for resources configured in [HCP](https://portal.cloud.hashicorp.com/) and execute them in your VPC. It will scan any available jobs, otherwise it will sleep and wait for a job to be queued in HCP.

## Installation
The Agent is currently a subcommand of the `vault-radar` CLI. To use the Agent, please install or update to the latest CLI. [See here for instructions](https://developer.hashicorp.com/hcp/docs/vault-radar/cli#download-and-install-cli).

## Usage

In order to run the `agent` in your environment there are 3 configuration steps required in HCP and your local environment.

### Create a Service Principal

You will need to log into the HCP web portal to create your Service Principals. You can follow the HCP docs to create your [Project Service Principals](https://developer.hashicorp.com/hcp/docs/hcp/admin/iam/service-principals#project-level-service-principals-1). You will need to create the Service Principals at Admin level, more information about this level contained in [these](https://developer.hashicorp.com/hcp/docs/hcp/admin/iam/users#project-role) HCP docs. You will also need to generate a [service principal key](https://developer.hashicorp.com/hcp/docs/hcp/admin/iam/service-principals#generate-a-service-principal-key) **that gives you a Client Id and Client Secret that you will use in the next few steps**.

### Create an Agent Pool in the HCP Portal

> **_Note:_** Before you create a agent, there is currently no way to delete agents via the UI

From the settings page, there will be an `Agent` tab. Select and follow the instructions to create a new Agent Pool. Alternatively attempting to onboard a new agent data source will direct you to create an Agent Pool if you have not already.

### Configure your Local Environment

To run agent you will need your client id and client secret from the service principal you just created, as well as your project and agent pool id, which will be provided to you during your agent pool creation flow.

To run the agent, the following environment variables must be set:

```bash
export HCP_PROJECT_ID=<HCP_PROJECT_ID>
export HCP_CLIENT_ID=<HCP_CLIENT_ID>
export HCP_CLIENT_SECRET=<HCP_CLIENT_SECRET>

# The Agent Pool Id that was provided after agent pool creation flow via UI
export HCP_RADAR_AGENT_POOL_ID=<AGENT_POOL_ID>
```

Your HCP Project ID can also be found by selecting your project --> `Project Settings` --> `Project ID`.

#### Configure Secret Values
For most Data Sources the agent is going to need some kind of token or secret to authenticate with the Data Source itself for scanning. When onboarding your Data Source on HCP, you may be prompted to configure the secret. The agent is expecting a URI. Currently the only format supported is a URI for an Environment Variable, which looks like this: `env://ENV_VARIABLE_NAME`. If for example we are configuring a GitHub Data Source, we are going to need to generate a GitHub PAT for the Agent to use. And then the value of the PAT is going to be stored locally where the Agent runs as an Environment Variable. If you saved the environment variable as `VAULT_RADAR_GIT_TOKEN` then the vaule you should enter in HCP is `env://VAULT_RADAR_GIT_TOKEN`.

## Running the Agent

Now that our environment is configured, we're ready to run the agent locally. Use the following command to start the agent:

```bash
vault-radar agent exec
```

## Add a Data Source for the Agent to Monitor

Now that agent is up and running, we can onboard a Data Source and select Resources to be scanned. Navigate to the `Data Sources` tab in the HCP Vault Radar web portal. Then choose to add an Agent Data Source. Select the Data Source type and provide the information requested. If the information is all correct, you will be prompted to either monitor all of the resources or the agent can enumerate resources and you select the resources it should monitor. Once that is complete, the scans will be scheduled and the Agent will begin scanning any requested resources.

**Note that you should not configure a Data Source that is being scanned by SaaS for agent.**

### View Events

After the scan, all the events are populated under the events tab.

### Currently Supported Scan Data Sources

- [`scan repo`](https://developer.hashicorp.com/hcp/docs/vault-radar/cli/scan/repo)
