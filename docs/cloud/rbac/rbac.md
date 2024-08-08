# RBAC (Private Beta)

Vault radar supports RBAC at the resource level, allowing admin users to manage the access of a group's permissions to individual resources.


## Setup Overview

1. [Create a group for the organization](#create-a-group-for-the-organization)
2. [Add members to the group](#add-members-to-the-group)
3. [Create a project level group](#create-a-project-level-group)
4. [Assign a Vault Radar developer role to the group](#assign-a-vault-radar-developer-role-to-the-group)
5. [Add Vault Radar resources to the project level group](#add-vault-radar-resources-to-a-project-level-group)

### Create a group for the organization
1. Navigate to the organizations page within HCP and click on an organization ![](img/1-RBAC.png)
2. Within the organization, navigate to the Access Control page ![](img/2-RBAC.png)
3. Within the access control page for the organization, navigate to the Groups page ![](img/3-RBAC.png)
4. Click create group ![](img/4-RBAC.png)
5. Enter a name for the group and submit ![](img/5-RBAC.png)

### Add members to the group
6. Click Add Members ![](img/6-RBAC.png)
7. Select your group members and click Submit ![](img/7-RBAC.png)

### Create a project level group
8. Navigate to a project page within your organization ![](img/8-RBAC.png)
9. Click on a project within your organization ![](img/9-RBAC.png)
10. Within the project, navigate to the Access Control page ![](img/10-RBAC.png)
11. Within the access control page of the project, navigate to the Groups page ![](img/11-RBAC.png)
12. Within the Groups page, click "Add Groups" ![](img/12-RBAC.png)
13. Select the organization level group(s) that you would like to add and click "Add Selected Groups" ![](img/13-RBAC.png)

### Assign a Vault Radar developer role to the group
14. Click on the select service dropdown ![](img/14-RBAC.png)
15. Select Vault Radar service from the dropdown ![](img/15-RBAC.png)
16. Click on the select role dropdown ![](img/16-RBAC.png)
17. Select the Vault Radar Developer role from dropdown ![](img/17-RBAC.png)
18. Click Add Groups  ![](img/18-RBAC.png) 
You now have a project configured to use Vault Radar RBAC ![](img/19-RBAC.png)

### Add Vault Radar resources to a project level group
19. Within the Vault Radar application, navigate to Resources ![](img/1-RBAC-IN-APP.png)
20. Select the resources that you wish to setup RBAC for and click "Add RBAC" ![](img/2-RBAC-IN-APP.png)
20. Select the project level group that you wish to give access to the resource(s) ![](img/3-RBAC-IN-APP.png)
20. Select the role to apply for the Resource and Group ![](img/4-RBAC-IN-APP.png)
The Resource(s) now have RBAC applied ![](img/5-RBAC-IN-APP.png)
