# RBAC (Private Beta)

Vault radar supports RBAC at the resource level, allowing admin users to manage the access of a group's permissions to individual resources.

## Setup Overview
1. [Create a group for the organization](#create-a-group-for-the-organization)
2. [Add members to the group](#add-members-to-the-group)
3. [Create a project level group](#create-a-project-level-group)
4. [Assign a Vault Radar developer role to the group](#assign-a-vault-radar-developer-role-to-the-group)
5. [Add Vault Radar resources to the project level group](#add-vault-radar-resources-to-a-project-level-group)

### Create a group for the organization
1. Navigate to the organizations page within HCP and click on an organization ![](img/GROUP-RBAC-SETUP-1.png)
2. Within the organization, navigate to the Access Control page ![](img/GROUP-RBAC-SETUP-2.png)
3. Within the access control page for the organization, navigate to the Groups page ![](img/GROUP-RBAC-SETUP-3.png)
4. Click create group ![](img/GROUP-RBAC-SETUP-4.png)
5. Enter a name for the group and submit ![](img/GROUP-RBAC-SETUP-5.png)

### Add members to the group
6. Click Add Members ![](img/GROUP-RBAC-SETUP-6.png)
7. Select your group members and click Submit ![](img/GROUP-RBAC-SETUP-7.png)

### Create a project level group
8. Navigate to a project page within your organization ![](img/GROUP-RBAC-SETUP-8.png)
9. Click on a project within your organization ![](img/GROUP-RBAC-SETUP-9.png)
10. Within the project, navigate to the Access Control page ![](img/GROUP-RBAC-SETUP-10.png)
11. Within the access control page of the project, navigate to the Groups page ![](img/GROUP-RBAC-SETUP-11.png)
12. Within the Groups page, click "Add Groups" ![](img/GROUP-RBAC-SETUP-12.png)
13. Select the organization level group(s) that you would like to add and click "Add Selected Groups" ![](img/GROUP-RBAC-SETUP-13.png)

### Assign a Vault Radar developer role to the group
14. Click on the select service dropdown ![](img/GROUP-RBAC-SETUP-14.png)
15. Select Vault Radar service from the dropdown ![](img/GROUP-RBAC-SETUP-15.png)
16. Click on the select role dropdown ![](img/GROUP-RBAC-SETUP-16.png)
17. Select the Vault Radar Developer role from dropdown ![](img/GROUP-RBAC-SETUP-17.png)
18. Click Add Groups  ![](img/GROUP-RBAC-SETUP-18.png) 
You now have a project configured to use Vault Radar RBAC ![](img/GROUP-RBAC-SETUP-19.png)

### Add Vault Radar resources to a project level group
19. Within the Vault Radar application, navigate to Resources ![](img/RBAC-IN-APP-1.png)
20. Select the resources that you wish to setup RBAC for and click "Add RBAC" ![](img/RBAC-IN-APP-2.png)
20. Select the project level group that you wish to give access to the resource(s) ![](img/RBAC-IN-APP-3.png)
20. Select the role to add the resource to the group ![](img/RBAC-IN-APP-4.png)
The Resource(s) are now a part of the project level group ![](img/RBAC-IN-APP-5.png)

### Remove Vault Radar resources from a project level group
1. Within the Vault Radar application, navigate to Resources ![](img/RBAC-IN-APP-1.png)
2. Select the resources that you wish to setup RBAC for and click "Add RBAC" ![](img/RBAC-REMOVE-1.png)
3. Select the resources that you wish to setup RBAC for and click "Add RBAC" ![](img/RBAC-REMOVE-2.png)
The Resource(s) are no longer a part of the project level group ![](img/RBAC-IN-APP-5.png)

### Accessing a resource once RBAC has been applied
1. Navigate to the Vault Radar product and click the dropdown ![](img/RBAC-SELECT-RESOURCE-1.png)
2. Select your resource and click "View Scan Events" ![](img/RBAC-SELECT-RESOURCE-2.png)
You can now view events within the selected resource ![](img/RBAC-VIEWER-EVENTS.png)

### Accessing a resource as a non-admin user without any RBAC applied
If you are attempting to access radar on a project where you are not an admin user, you will see the following screen:  ![](img/RBAC-NO-PERMS.png)
