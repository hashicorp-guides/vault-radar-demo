# RBAC (Private Beta)

Vault radar supports RBAC at the resource level, allowing admin users to manage the access of a group's permissions to individual resources.

## Setup Overview
1. [Create a group for the organization](#create-a-group-for-the-organization)
2. [Add members to the group](#add-members-to-the-group)
3. [Create a project level group](#create-a-project-level-group)
4. [Assign a Vault Radar developer role to the group](#assign-a-vault-radar-developer-role-to-the-group)
5. [Add Vault Radar resources to the project level group](#add-vault-radar-resources-to-a-project-level-group)

## Additional guides
- [Removing Vault Radar resources from a project level group](#removing-vault-radar-resources-from-a-project-level-group)
- [Accessing a Vault Radar resource once RBAC has been applied](#accessing-a-vault-radar-resource-once-rbac-has-been-applied)
- [Accessing a Vault Radar resource as a non-admin user without any RBAC applied](#accessing-a-vault-radar-resource-as-a-non-admin-user-without-any-rbac-applied)

### Create a group for the organization
1. Navigate to the organizations page within HCP and click on an organization ![](img/GROUP-RBAC-SETUP-1.png)
2. Within the organization, navigate to the Access Control page ![](img/GROUP-RBAC-SETUP-2.png)
3. Within the access control page for the organization, navigate to the Groups page ![](img/GROUP-RBAC-SETUP-3.png)
4. Click create group ![](img/GROUP-RBAC-SETUP-4.png)
5. Enter a name for the group and submit ![](img/GROUP-RBAC-SETUP-5.png)

---

### Add members to the group
**In order for the assigned group member to have RBAC enforced, the user must not have any role assigned role at the organization or project level**
1. Click Add Members ![](img/GROUP-RBAC-SETUP-6.png)
2. Select your group members and click "Add group members" ![](img/GROUP-RBAC-SETUP-7.png)

---

### Create a project level group
1. Navigate to a project page within your organization ![](img/GROUP-RBAC-SETUP-8.png)
2. Click on a project within your organization ![](img/GROUP-RBAC-SETUP-9.png)
3. Within the project, navigate to the Access Control page ![](img/GROUP-RBAC-SETUP-10.png)
4. Within the access control page of the project, navigate to the Groups page ![](img/GROUP-RBAC-SETUP-11.png)
5. Within the Groups page, click "Add groups" ![](img/GROUP-RBAC-SETUP-12.png)
6. Select the organization level group(s) that you would like to add and click "Add selected groups" ![](img/GROUP-RBAC-SETUP-13.png)

---

### Assign a Vault Radar developer role to the group
1. Click on the select service dropdown ![](img/GROUP-RBAC-SETUP-14.png)
2. Select "Vault Radar" service from the dropdown ![](img/GROUP-RBAC-SETUP-15.png)
3. Click on the select role dropdown ![](img/GROUP-RBAC-SETUP-16.png)
4. Select the "Vault Radar Developer" role from dropdown ![](img/GROUP-RBAC-SETUP-17.png)
5. Click "Add groups"  ![](img/GROUP-RBAC-SETUP-18.png) 
You now have a project configured to use Vault Radar RBAC ![](img/GROUP-RBAC-SETUP-19.png)

---

### Add Vault Radar resources to a project level group
1. Within the Vault Radar application, navigate to Resources ![](img/RBAC-IN-APP-1.png)
2. Select the resources that you wish to setup RBAC for and click "Assign Groups" ![](img/RBAC-IN-APP-2.png)
3. Select the project level group that you wish to give access to the resource(s) ![](img/RBAC-IN-APP-3.png)
4. Select the role to add the resource to the group ![](img/RBAC-IN-APP-4.png)
The Resource(s) are now a part of the project level group ![](img/RBAC-IN-APP-5.png)

---

### Vault Radar resource roles

Within Vault Radar, we offer two different roles when assigning a group to a resource:
- Resource Viewer
  - Can only view events for a given resource
- Resource Contributor
  - Can view and modify the state of events for a given resource

---

### Removing Vault Radar resources from a project level group
1. Within the Vault Radar application, navigate to Resources ![](img/RBAC-IN-APP-1.png)
2. Select the resource that you wish to remove from the group ![](img/RBAC-REMOVE-1.png)
3. Click the trash can icon next to the group in the details pane for the resource ![](img/RBAC-REMOVE-2.png)

---

### Accessing a Vault Radar resource once RBAC has been applied
1. Navigate to the Vault Radar product and click the dropdown ![](img/RBAC-SELECT-RESOURCE-1.png)
2. Select your resource and click "View scan results" ![](img/RBAC-SELECT-RESOURCE-2.png)
You can now view events within the selected resource, if you would like to change your resource, select the Resource dropdown and choose a different option ![](img/RBAC-VIEWER-EVENTS.png)

---

### Accessing a Vault Radar resource as a non-admin user without any RBAC applied
If you are attempting to access radar on a project where you are not an admin user, you will see the following screen:  ![](img/RBAC-NO-PERMS.png)
