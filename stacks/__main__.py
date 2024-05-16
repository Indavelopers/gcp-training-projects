"""A Google Cloud Python Pulumi program"""

import pulumi
import pulumi_gcp as gcp
import hashlib
import importlib
import random


# Config
config = pulumi.Config()
organization_id = config.require('organization_id')
billing_account_id = config.require('billing_account_id')
folder_name  = config.require('folder_name')
folder_display_name = config.require('folder_display_name')
project_prefix = config.require('project_prefix')
emails = config.require_object('emails')
roles = config.require_object('roles')
apis = config.require_object('apis')
infra_script = config.require('infra_script')
n_students = len(emails)


# Create a GCP folder for the training projects
folder = gcp.organizations.Folder(folder_name, display_name=folder_display_name, parent=f'organizations/{organization_id}')

# Create GCP projects under said folder
# It's recommended to create n_students + 1 projects, having "project_prefix-0-suffix" for the instructor
# Set the seed for random numbers so each run generates same numbers for same emails/projects
random.seed('test')
random_numbers = [str(random.randint(0, 99)).zfill(2) for _ in range(n_students)]

generated_project_ids = [project_prefix + '-' + random_number + '-' + hashlib.sha256(email.encode()).hexdigest()[:4] 
                 for random_number, email in zip(random_numbers, emails)]

gcp_project_ids = []
for gcp_project_id in generated_project_ids:
    project = gcp.organizations.Project(gcp_project_id, name=gcp_project_id, project_id=gcp_project_id, folder_id=folder.id, billing_account=billing_account_id)

    gcp_project_ids.append(project.id)    # Pulumi resource name = GCP project ID = GCP project name

pulumi.export('folder_id', folder.id)
pulumi.export('project_ids', gcp_project_ids)

# Enable APIs on projects
for gcp_project_id, generated_project_id in zip(gcp_project_ids, generated_project_ids):
    for api in apis:
        project_api = gcp.projects.Service(generated_project_id + '-' + api, project=gcp_project_id, service=api)

pulumi.export('apis', apis)

# Setup IAM for the students
for gcp_project_id, generated_project_id, email in zip(gcp_project_ids, generated_project_ids, emails):    
    for role in roles:
        project_binding = gcp.projects.IAMMember(generated_project_id + '-' + role, project=gcp_project_id, role=role, member=f'user:{email}')

pulumi.export('emails', emails)
pulumi.export('roles', roles)

# Create template resources for the lab
importlib.import_module(infra_script)
