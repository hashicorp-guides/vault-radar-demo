# station (Private Beta)

A hybrid station has the capability to scan a resource within your Virtual Private Cloud (VPC) environment based on the inputs provided through the HCP UI.
The `station` command is used to fetch scan jobs from [HCP](https://portal.cloud.hashicorp.com/) and execute them in your VPC. It will scan any available jobs, otherwise it will sleep and wait for a job to be queued in HCP.

## Setting Up

In order to run `station` in your environment there are 3 configuration steps required in HCP and your local environment.

### Create a Service Principal

You will need to log into the HCP web portal to create your Service Principals. You can follow the HCP docs to create your [Project Service Principals](https://developer.hashicorp.com/hcp/docs/hcp/admin/iam/service-principals#project-level-service-principals-1). You will need to create the Service Principals at Admin level, more information about this level contained in [these](https://developer.hashicorp.com/hcp/docs/hcp/admin/iam/users#project-role) HCP docs. You will also need to generate a [service principal key](https://developer.hashicorp.com/hcp/docs/hcp/admin/iam/service-principals#generate-a-service-principal-key) that gives you a client id and client secret that you will use in the next few steps.

### Create a Station in the HCP Portal

> **_Note:_** Before you create a station, there is currently no way to delete stations via the UI

Now, you will need to initiate a station in the HCP web portal. If it's your first time using `Vault Radar` in HCP, you will need to configure a data source of your choice in order to get the `Station` tab view. This data source will not be used for running the station at all. This is a known UX issue that will be fixed in a future iteration.

Once you have the `Station` tab view, you can start working through the station creation flow. This will give you a Station ID you will use in your local environment.

### Configure your Local Environment

To run station you will need your client id and client secret from the service principal you just created, as well as your project and station id, which will be provided to you during your station creation flow.

To run station, the following environment variables must be set:

```bash
export HCP_PROJECT_ID=<HCP_PROJECT_ID>
export HCP_CLIENT_ID=<HCP_CLIENT_ID>
export HCP_CLIENT_SECRET=<HCP_CLIENT_SECRET>

# The Station Id that was provided after creation
export HCP_RADAR_STATION_ID=<STATION_ID>
```

You will also need to ensure you hae the proper environment variable set for authentication to git. You can use the following [docs](https://github.com/hashicorp-guides/vault-radar-demo/blob/main/docs/git.md#authentication) to set your git auth token

Your HCP Project ID can also be found by selecting your project --> `Project Settings` --> `Project ID`.

## Running Station

Now that our environment is configured, we're ready to run the station locally. Use the following command to start the station:

```bash
vault-radar station setup
```

This command has no local output but is still running in the background, waiting for jobs. You can follow the log file for debugging if you run into issues.

## Creating a Station Resource

Now that station is up and running, we can add a resource to be scanned. In the `Station` tab in the HCP web portal, select `Add resource to station`, which will prompt you to add a Git URL as your resource. Your locally running Station will pull this job, scan it, and upload events to HCP. You can view your newly added resource in the `Resources` pane.

### View Events

After the scan, all the events are populated under the events tab.

### Currently Supported Scan Data Sources

- [`scan-repo`](git.md)
