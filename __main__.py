"""A Google Cloud Python Pulumi program"""

import pulumi
import pulumi_gcp as gcp

from resources import create_resources


# Config
config = pulumi.Config()
organization_id = config.require('organization_id')
billing_account_id = config.require('billing_account_id')
folder_name  = config.require('folder_name')
folder_display_name = config.require('folder_display_name')
project_prefix = config.require('project_prefix')
project_random_suffix = config.require('project_random_suffix')
emails = config.require_object('emails')
roles = config.require_object('roles')
apis = config.require_object('apis')
n_students = len(emails)


# It's recommended to create n_students + 1 projects, having "project_prefix-0-suffix" for the instructor
project_names = [project_prefix + '-' + str(i) for i in range(n_students)]

# Create a GCP folder for the training projects
folder = gcp.organizations.Folder(folder_name, display_name=folder_display_name, parent=f'organizations/{organization_id}')

# Create GCP projects under said folder
project_ids = []
for project_name in project_names:
    project_id = project_name + '-' + project_random_suffix
    project_ids.append(project_id)

    project = gcp.organizations.Project(project_id, name=project_name, project_id=project_id, folder_id=folder.name, billing_account=billing_account_id)

pulumi.export('folder_id', folder.name)
pulumi.export('project_ids', project_ids)


# Enable APIs on projects
# todo: enable apis

pulumi.export('apis', apis)


# Setup IAM for the students
for project_id, email in zip(project_ids, emails):    
    for role in roles:
        project_binding = gcp.projects.IAMMember(project_id, project=project_id, role=role, member=f'user:{email}')

pulumi.export('emails', emails)
pulumi.export('roles', roles)


# Create template resources for the lab
create_resources(project_ids)
