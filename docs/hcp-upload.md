# HCP Upload

For commands that HCP upload is enabled you will need to go through the following configuration steps within your environment in order to upload.

## Creating your Service Principals

You wil need to log into the HCP web portal to create your service principals. You can follow the HCP docs in order to create your [Project Service Principals](https://developer.hashicorp.com/hcp/docs/hcp/admin/iam/service-principals#project-level-service-principals-1). You will need to create the Service Principals at Admin level, more information about this level contained in [these](https://developer.hashicorp.com/hcp/docs/hcp/admin/iam/users#project-role) HCP docs.

Note: be sure to Copy the Client Secret on creation as you will be unable to retrieve it later.

## Prepare your Environment

You will need to set the following environment variables for your CLI runtime referencing the newly created Service Principles.

```bash
export HCP_PROJECT_ID=<HCP_PROJECT_ID>
export HCP_CLIENT_ID=<HCP_CLIENT_ID>
export HCP_CLIENT_SECRET=<HCP_CLIENT_SECRET>
```

### Currently supported Scan Data Sources

* [`scan-confluence`](confluence.md)
* [`scan-repo`](git.md)
